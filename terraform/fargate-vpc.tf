data "aws_vpc" "fargate-vpc" {
  id = "vpc-05a0c2d68352a2ef4"
}

locals {
  container_port = 9000
}

data "aws_subnet" "bebop_subnet" {
  id = "subnet-004c03d9e2b09481f"
}
