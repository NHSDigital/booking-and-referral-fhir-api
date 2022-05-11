data "aws_vpc" "fargate-vpc" {
  id = "vpc-05a0c2d68352a2ef4"
}

locals {
  container_port = 9000
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

resource "aws_subnet" "main" {
  vpc_id     = data.aws_vpc.fargate-vpc.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = local.name_prefix
  }
}  

resource "aws_vpc_endpoint" "ecr_dkr" {
  vpc_id       = data.aws_vpc.fargate-vpc.id
  service_name = "com.amazonaws.${var.region}.ecr.dkr"
  vpc_endpoint_type = "Interface"
  private_dns_enabled = true
  subnet_ids          = [aws_subnet.main.id]
security_group_ids = [
    "${aws_security_group.ecs_tasks.id}",
  ]
tags = {
    Name = "${local.name_prefix}-ecr"
    
  }


}

resource "aws_vpc_endpoint" "cloudwatch_logs" {
  vpc_id       = data.aws_vpc.fargate-vpc.id
  service_name = "com.amazonaws.${var.region}.logs"
  vpc_endpoint_type = "Interface"
  subnet_ids          = [aws_subnet.main.id]
security_group_ids = [
    "${aws_security_group.ecs_tasks.id}",
  ]
tags = {
    Name = "${local.name_prefix}-logs"
    
  }


}

resource "aws_vpc_endpoint" "s3" {
  vpc_id       = data.aws_vpc.fargate-vpc.id
  service_name = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"

  route_table_ids = ["rtb-0618565988622142e"]

tags = {
    Name = "${local.name_prefix}-s3"
    
  }


}