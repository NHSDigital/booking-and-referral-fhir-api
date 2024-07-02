resource "aws_apigatewayv2_vpc_link" "alb_vpc_link" {
    name               = local.name_prefix
    security_group_ids = [aws_security_group.vpc_link_security_group.id]
    subnet_ids         = module.private_subnets[*].subnet_id
}

resource "aws_security_group" "vpc_link_security_group" {
    name   = "${local.name_prefix}-vpc-link"
    vpc_id = var.vpc_id

    egress {
        protocol    = "tcp"
        from_port   = var.listener_port
        to_port     = var.listener_port
        cidr_blocks = local.private_subnet_cidr
    }

    ingress {
        protocol    = "tcp"
        from_port   = var.listener_port
        to_port     = var.listener_port
        cidr_blocks = local.public_subnet_cidr
    }
}
