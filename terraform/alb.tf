module "alb" {
  source = "./alb"

  name_prefix          = local.name_prefix
  container_port       = var.container_port
  infra_private_subnet = local.private_subnet_cidr
  infra_public_subnet  = local.public_subnet_cidr
  listener_port        = 80
  public_subnet_ids    = local.public_subnet_ids
  vpc_id               = local.vpc_id
}
