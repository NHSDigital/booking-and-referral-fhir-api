resource "aws_ecr_repository" "fargate_registry" {
  count = length(var.registries)
  name  = "${local.name_prefix}-${var.registries[count.index]}"
}
