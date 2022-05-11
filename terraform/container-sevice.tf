resource "aws_ecs_service" "mock-receiver-service" {
  name            = "${local.name_prefix}-service"
  cluster         = aws_ecs_cluster.ecs-cluster.id
  task_definition = aws_ecs_task_definition.mock-receiver.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = [data.aws_subnet.bebop_subnet.id]
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


resource "aws_security_group" "ecs_tasks" {
  name   = "${local.name_prefix}-sg-task"
  vpc_id = data.aws_vpc.fargate-vpc.id

  ingress {
    protocol         = "tcp"
    from_port        = local.container_port
    to_port          = local.container_port
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}
