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

data "aws_subnet" "public_subnets" {
  count = length(local.public_subnet_ids)
  id    = local.public_subnet_ids[count.index]
}

data "aws_subnet" "private_subnets" {
  count = length(local.private_subnet_ids)
  id    = local.private_subnet_ids[count.index]
}

locals {
    public_subnet_ids   = data.terraform_remote_state.bebop-infra.outputs.public_subnet_ids
    public_subnet_cidr  = data.aws_subnet.public_subnets.*.cidr_block
    private_subnet_ids  = data.terraform_remote_state.bebop-infra.outputs.private_subnet_ids
    private_subnet_cidr = data.aws_subnet.private_subnets.*.cidr_block
}

locals {
  vpc_link_id      = data.terraform_remote_state.bebop-infra.outputs.vpc_link_id
}

locals {
  cert_storage_bucket = data.terraform_remote_state.bebop-infra.outputs.cert_storage_bucket
}
