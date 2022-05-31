module "alb" {
    source               = "./alb"
    name_prefix          = local.name_prefix
    vpc_id               = var.vpc_id
    public_subnet_ids    = module.subnets[*].subnet_id
    infra_public_subnet  = local.public_subnet_cidr
    infra_private_subnet = local.private_subnet_cidr
    vpc_cidr             = local.vpc_cidr
    container_port       = var.container_port
    listener_port        = var.listener_port
}
