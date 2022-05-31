resource "aws_lb" "alb" {
    name               = var.name_prefix
    internal           = true
    load_balancer_type = "application"

    subnets         = var.public_subnet_ids
    security_groups = [aws_security_group.alb_security_group.id]
}
