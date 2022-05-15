module "mock-receiver" {
  source      = "./mock-receiver"
  region      = var.region
  name_prefix = local.name_prefix

  vpc_id     = local.vpc_id
  cluster_id = local.fargate_cluster_id
  subnet_ids = local.fargate_subnets_ids

  container_port  = 9000
  image_version   = local.environment
  repository_url  = local.mock_receiver_repository_url
  repository_name = local.mock_receiver_repository_name
}
