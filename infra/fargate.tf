module "fargate" {
    source      = "./fargate"
    region      = var.region
    name_prefix = local.name_prefix
    vpc_id      = var.vpc_id
    subnets     = local.private_subnet
}

