output "vpc_id" {
  value = var.vpc_id
}

output "vpc_link_id" {
  value = aws_apigatewayv2_vpc_link.alb_vpc_link.id
}

output "private_subnet_ids" {
  value = module.private_subnets[*].subnet_id
}

output "fargate_subnet_ids" {
  value = module.private_subnets[*].subnet_id
}

output "cert_storage_bucket" {
  value = aws_s3_bucket.cert_storage.bucket
}
