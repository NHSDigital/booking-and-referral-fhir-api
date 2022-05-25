module "alb" {
    source            = "./alb"
    name_prefix       = local.name_prefix
    vpc_id            = var.vpc_id
    public_subnet_ids = module.subnets[*].subnet_id
}
