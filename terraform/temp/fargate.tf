resource "aws_ecs_cluster" "ecs-cluster" {
  name = "${local.name_prefix}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  # configuration {
  # execute_command_configuration {
  #   logging    = "OVERRIDE"

  #   log_configuration {
  #     cloud_watch_log_group_name     = aws_cloudwatch_log_group.cluster_container_logs.name
  #   }
  # }
  #}
}

# resource "aws_cloudwatch_log_group" "cluster_container_logs" {
#   name = "${local.name_prefix}-cluster"
# }


