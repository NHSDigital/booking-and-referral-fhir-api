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

output "nlb_listener_arn_http" {
    value = aws_lb_listener.nlb_listener.arn
}

output "vpc_link_id" {
    value = aws_apigatewayv2_vpc_link.alb_vpc_link.id
}
