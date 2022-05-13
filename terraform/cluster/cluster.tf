resource "aws_ecs_cluster" "fargate-cluster" {
  name = var.name_prefix
}
