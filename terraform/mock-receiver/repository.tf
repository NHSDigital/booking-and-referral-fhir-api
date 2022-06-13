resource "aws_ecr_repository" "mock_receiver_registry" {
  name = var.name_prefix
}
