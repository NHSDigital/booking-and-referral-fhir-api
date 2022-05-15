resource "aws_cloudwatch_log_group" "container_log_group" {
  name              = "${var.name_prefix}-container"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_stream" "container_log_stream" {
  name           = "mock-receiver"
  log_group_name = aws_cloudwatch_log_group.container_log_group.name
}
