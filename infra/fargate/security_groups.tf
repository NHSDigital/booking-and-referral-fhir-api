locals {
  subnets_cidr = [for subnet in var.subnets : subnet.cidr]
}

resource "aws_security_group" "vpc_endpoint_sg" {
  name   = "${var.name_prefix}-vpc_endpoint_sg"
  vpc_id = var.vpc_id

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = local.subnets_cidr
  }
}
