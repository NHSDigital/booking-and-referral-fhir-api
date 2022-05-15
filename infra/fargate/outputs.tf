output "cluster_id" {
  value = module.cluster.cluster_id
}

output "subnet_ids" {
  value = aws_subnet.private_subnets.*.id
}
