resource "aws_apigatewayv2_vpc_link" "alb_vpc_link" {
    name               = local.name_prefix
    security_group_ids = [aws_security_group.vpc_link_security_group.id]
    // vpc_link should be used to connect the private resources i.e. resources in private subnets
    subnet_ids         = module.subnets[*].subnet_id
}

// TODO: narrow down security
resource "aws_security_group" "vpc_link_security_group" {
    name   = "${local.name_prefix}-vpc-link"
    vpc_id = var.vpc_id

    egress {
        protocol    = "-1"
        from_port   = 0
        to_port     = 0
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        protocol    = "-1"
        from_port   = 0
        to_port     = 0
        cidr_blocks = ["0.0.0.0/0"]
    }
}
