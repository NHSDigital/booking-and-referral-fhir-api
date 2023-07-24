resource "aws_lb" "alb" {
  name               = var.short_prefix
  internal           = true
  load_balancer_type = "application"

  subnets         = var.private_subnet_ids
  security_groups = [aws_security_group.alb_security_group.id]

  access_logs {
    bucket  = aws_s3_bucket.lb_logs.bucket
    enabled = true
  }
}
