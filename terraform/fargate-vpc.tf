data "aws_vpc" "fargate-vpc" {
  id = data.terraform_remote_state.bebop-infra.outputs.bebop-dev-vpc_id
}

locals {
  container_port = 9000
}

data "aws_subnet" "bebop_private_subnet" {
  id = data.terraform_remote_state.bebop-infra.outputs.bebop-dev-private_subnet
}

data "aws_subnet" "bebop_public_subnet" {
  id = data.terraform_remote_state.bebop-infra.outputs.bebop-dev-public_subnet
}
