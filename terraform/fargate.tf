resource "aws_ecs_cluster" "ecs-cluster" {
  name = "${local.name_prefix}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

    configuration {
    execute_command_configuration {
      logging    = "OVERRIDE"
      
      log_configuration {
        cloud_watch_log_group_name     = aws_cloudwatch_log_group.cluster_container_logs.name
      }
    }
  }
}

resource "aws_cloudwatch_log_group" "cluster_container_logs" {
  name = "${local.name_prefix}-cluster"
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
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  
  container_definitions = jsonencode([
    {
      name         = "rest-api"
      image        = "${data.aws_ecr_image.sandbox_image.repository_name}:latest"
      essential    = true
      
      portMappings = [
        {
          containerPort = 9000
          hostPort      = 9000
          
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
  launch_type     = "FARGATE"
  network_configuration {
   security_groups  = [aws_security_group.ecs_tasks.id]
   subnets          = [aws_subnet.main.id]
   assign_public_ip = false
 }

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

