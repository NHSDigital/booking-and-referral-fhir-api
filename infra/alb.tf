resource "aws_lb" "application_load_balancer" {
    load_balancer_type = "application"
    subnets            = aws_subnet.public_subnets.*.id
    security_groups    = [aws_security_group.nlb_security_group.id]

    enable_cross_zone_load_balancing = true

    tags = {
        Name = local.name_prefix
    }
}


