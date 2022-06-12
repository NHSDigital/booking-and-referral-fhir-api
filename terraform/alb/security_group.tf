resource "aws_security_group" "alb_security_group" {
    name   = "${var.name_prefix}-alb"
    vpc_id = var.vpc_id

    egress {
        protocol    = "tcp"
        from_port   = var.container_port
        to_port     = var.container_port
        cidr_blocks = var.infra_private_subnet
    }

    ingress {
        protocol    = "tcp"
        from_port   = var.listener_port
        to_port     = var.listener_port
        cidr_blocks = var.infra_public_subnet
    }
}
