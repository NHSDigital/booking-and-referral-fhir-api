data "aws_vpc" "fargate-vpc" {
  id = data.terraform_remote_state.bebop-infra.outputs.bebop-dev-vpc_id
}

module "fargate" {
  source      = "./fargate"
  name_prefix = local.name_prefix
  vpc_id      = data.aws_vpc.fargate-vpc.id
}
