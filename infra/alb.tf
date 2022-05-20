data "aws_elb_service_account" "main" {}

resource "aws_s3_bucket" "alb_logs_bucket" {
    bucket = "${local.name_prefix}-alb-logs"
    policy = <<POLICY
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Principal": {
                "AWS": "arn:aws:iam::elb-account-id:root"
              },
              "Action": "s3:PutObject",
              "Resource": "arn:aws:s3:::"${local.name_prefix}-alb-logs"/prefix/AWSLogs/*"
            }
          ]
        }
        POLICY
}


resource "aws_lb" "application_load_balancer" {
    load_balancer_type = "application"
    subnets            = aws_subnet.public_subnets.*.id
    security_groups    = [aws_security_group.nlb_security_group.id]

    enable_cross_zone_load_balancing = true

    access_logs {
        bucket  = aws_s3_bucket.alb_logs_bucket.bucket
        prefix  = "test-lb"
        enabled = true
    }

    tags = {
        Name = local.name_prefix
    }
}

resource "aws_lb_listener" "nlb_listener" {
    load_balancer_arn = aws_lb.application_load_balancer.arn

    protocol = "HTTP"
    port     = "80"

    default_action {
        type             = "forward"
        target_group_arn = aws_lb_target_group.nlb_target_group.arn
    }

    tags = {
        Name = local.name_prefix
    }
}

resource "aws_lb_target_group" "nlb_target_group" {

    port     = "80"
    protocol = "HTTP"
    vpc_id   = var.vpc_id

    depends_on = [
        aws_lb.application_load_balancer
    ]

    lifecycle {
        create_before_destroy = true
    }
}
