module "mock-receiver" {
  source      = "./mock-receiver"
  region      = var.region
  name_prefix = local.name_prefix

  vpc_id        = local.vpc_id
  cluster_id    = module.cluster.cluster_id
  subnet_ids    = local.private_subnet_ids

  container_port = 9000
  image_version  = local.environment
  alb_tg_arn     = module.alb.alb_target_group_arn
  service_domain_name = local.service_domain_name
}
