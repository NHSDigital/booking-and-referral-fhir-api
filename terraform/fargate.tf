resource "aws_ecs_cluster" "ecs-cluster" {
  name = "${local.name_prefix}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_iam_role" "ecs-task-role" {
  name = "${local.name_prefix}-ecs-task"

  assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "ecs-tasks.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}

resource "aws_ecs_task_definition" "mock-receiver" {
  family                = "${local.name_prefix}-task"
  container_definitions = jsonencode([
    {
      name         = "rest-api"
      image        = "${data.aws_ecr_image.sandbox_image.repository_name}:latest"
      cpu          = 10
      memory       = 512
      essential    = true
      portMappings = [
        {
          containerPort = 5050
          hostPort      = 80
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "mock-receiver-service" {
  name            = "${local.name_prefix}-service"
  cluster         = aws_ecs_cluster.ecs-cluster.id
  task_definition = aws_ecs_task_definition.mock-receiver.arn
  desired_count   = 1
  #  iam_role        = aws_iam_role.ecs-task-role.arn
  #  depends_on = [aws_iam_role.ecs-task-role]

  #  ordered_placement_strategy {
  #    type  = "binpack"
  #    field = "cpu"
  #  }

  #  load_balancer {
  #    #    target_group_arn = aws_lb_target_group.foo.arn
  #    container_name = "mongo"
  #    container_port = 8080
  #  }

  #  placement_constraints {
  #    type       = "memberOf"
  #    expression = "attribute:ecs.availability-zone in [us-west-2a, us-west-2b]"
  #  }
  #
}

