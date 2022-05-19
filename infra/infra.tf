data "aws_vpc" "bebop_vpc" {
  id = var.vpc_id
}

locals {
  vpc_cidr = data.aws_vpc.bebop_vpc.cidr_block
}

