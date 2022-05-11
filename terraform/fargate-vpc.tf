resource "aws_vpc" "fargate-vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    "Name" = local.name_prefix
     }

}
locals {
  container_port = 9000
}

resource "aws_security_group" "ecs_tasks" {
  name   = "${local.name_prefix}-sg-task"
  vpc_id = aws_vpc.fargate-vpc.id
 
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

resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.fargate-vpc.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = local.name_prefix
  }
}