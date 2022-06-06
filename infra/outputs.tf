output "vpc_id" {
  value = var.vpc_id
}

output "fargate_cluster_id" {
  value = module.fargate.cluster_id
}

output "fargate_subnet_ids" {
  value = module.fargate.subnet_ids
}

output "fargate_repository_url" {
    value = {for reg in var.registries : reg => aws_ecr_repository.fargate_registry[index(var.registries, reg)].repository_url}
}

output "fargate_repository_name" {
  value = {for reg in var.registries : reg => aws_ecr_repository.fargate_registry[index(var.registries, reg)].name}
}

output "alb_arn" {
  value = module.alb.alb_arn
}

output "vpc_link_id" {
  value = aws_apigatewayv2_vpc_link.alb_vpc_link.id
}

output "public_subnet_ids" {
  value = module.subnets[*].subnet_id
}

output "alb_tg_arn" {
  value = module.alb.alb_target_group_arn
}

output "alb_listener_arn" {
  value = module.alb.alb_listener_arn
}
