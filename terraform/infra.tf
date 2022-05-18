/* Use infra terraform state to populate infra outputs.
We use the infra state file to read the outputs and then reassign them to local names
*/

data "terraform_remote_state" "bebop-infra" {
  backend = "s3"
  config  = {
    bucket = "terraform-nhsd-apim-bebop-infra"
    key    = "infra"
    region = "eu-west-2"
  }
}

locals {
  vpc_id = data.terraform_remote_state.bebop-infra.outputs.vpc_id
}

# fargate outputs
locals {
  fargate_subnets_ids     = data.terraform_remote_state.bebop-infra.outputs.fargate_subnet_ids
  fargate_cluster_id      = data.terraform_remote_state.bebop-infra.outputs.fargate_cluster_id
  fargate_repository_url  = data.terraform_remote_state.bebop-infra.outputs.fargate_repository_url
  fargate_repository_name = data.terraform_remote_state.bebop-infra.outputs.fargate_repository_name
}

locals {
  repositories = ["mock-receiver"]

  mock_receiver_repository_url  = local.fargate_repository_url[local.repositories[0]]
  mock_receiver_repository_name = local.fargate_repository_name[local.repositories[0]]
}
