resource "aws_ecs_cluster" "aws-ecs-cluster" {
  name = "${var.app_name}-${var.environment}-cluster"
  tags = {
    Name        = "${var.app_name}-ecs"
    Environment = var.environment
  }
}

resource "aws_ecr_repository" "bars_container_registry" {
  name = "${var.app_name}-${var.environment}-ecr"
  tags = {
    Name        = "${var.app_name}-ecr"
    Environment = var.environment
  }
}
resource "aws_cloudwatch_log_group" "log-group" {
  name = "${var.app_name}-${var.environment}-logs"

  tags = {
    Application = var.app_name
    Environment = var.environment
  }
}

#      "image": "${aws_ecr_repository.bars_container_registry.repository_url}:latest",
resource "aws_ecs_task_definition" "aws-ecs-task" {
  family = "${var.app_name}-task"

  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  memory                   = "512"
  cpu                      = "256"
  task_role_arn = aws_iam_role.task_role.arn
  execution_role_arn = aws_iam_role.main_ecs_tasks.arn

  container_definitions = jsonencode([
    {
      name: "${var.app_name}-${var.environment}-container",
      image     = "vad1mo/hello-world-rest"
      cpu       = 256
      memory    = 512
      essential = true
      logConfiguration: {
        logDriver: "awslogs",
        options: {
          awslogs-group: aws_cloudwatch_log_group.log-group.id,
          awslogs-region: var.region,
          awslogs-stream-prefix: "${var.app_name}-${var.environment}"
        }
      },
      portMappings = [
        {
          containerPort = var.app_port
          hostPort      = var.app_port
        }
      ]
    }
  ])

  tags = {
    Name        = "${var.app_name}-ecs-td"
    Environment = var.environment
  }
}

resource "aws_ecs_service" "main" {
  name            = "${var.app_name}-${var.environment}-service"
  cluster         = aws_ecs_cluster.aws-ecs-cluster.id
  task_definition = aws_ecs_task_definition.aws-ecs-task.family
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    security_groups =[aws_security_group.ecs_tasks.id]
    subnets         = aws_subnet.private_subnets.*.id
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.nlb_tg.arn
    container_name   = "${var.app_name}-${var.environment}-container"
    container_port   = var.app_port
  }

  depends_on = [
    aws_ecs_task_definition.aws-ecs-task
  ]
}
