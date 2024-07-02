module "alb" {

  source = "./alb"
  name_prefix          = local.name_prefix
  short_prefix          = local.short_prefix
  container_port       = var.container_port
  infra_private_subnet = local.private_subnet_cidr
  listener_port        = 80
  private_subnet_ids    = local.private_subnet_ids
  vpc_id               = local.vpc_id
}
