resource "aws_ecs_task_definition" "mock-receiver" {
  family                   = var.name_prefix
  network_mode             = "awsvpc"
  // ARN of IAM role that allows your Amazon ECS container task to make calls to other AWS services.
  task_role_arn            = aws_iam_role.task_execution_role.arn
  //ARN of the task execution role that the Amazon ECS container agent and the Docker daemon can assume.
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512

  container_definitions = jsonencode([
    {
      name      = "mock-receiver"
      image     = "${var.repository_url}:${var.image_version}"
      essential = true

      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
        }
      ]

      logConfiguration : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-create-group" : "true",
          "awslogs-group" : "mockreceivertest"
          "awslogs-region" : var.region,
          "awslogs-stream-prefix" : "mockreceiver"
          //  "stoppedReason": "ResourceInitializationError: failed to validate logger args: : signal: killed"
        }
      }
    }
  ])
}
