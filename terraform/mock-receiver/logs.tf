resource "aws_cloudwatch_log_group" "container_log_group" {
  name              = "${var.name_prefix}-container"
  retention_in_days = 30
}
