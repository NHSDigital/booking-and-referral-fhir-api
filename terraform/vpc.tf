resource "aws_vpc" "bars_vpc" {
  cidr_block           = var.cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(local.tags, { Name = "${var.app_name}-${var.environment}-vpc" })
}

### VPC Network Setup

# Create the private subnets
resource "aws_subnet" "private_subnets" {
  count             = length(var.private_subnets)
  vpc_id            = aws_vpc.bars_vpc.id
  cidr_block        = element(var.private_subnets, count.index)
  availability_zone = element(var.availability_zones, count.index)

  tags = merge(local.tags, { Name = "${var.app_name}-${var.environment}-private-subnet-${count.index}" })
}

# Create the public subnets
# FIXME: We probably don't need this
resource "aws_subnet" "public_subnets" {
  count             = length(var.public_subnets)
  vpc_id            = aws_vpc.bars_vpc.id
  cidr_block        = element(var.public_subnets, count.index)
  availability_zone = element(var.availability_zones, count.index)

  tags = merge(local.tags, { Name = "${var.app_name}-${var.environment}-public-subnet-${count.index}" })
}

### Security Group Setup

# FIXME: These two SG has overlap with others in nlb and alb?
# ALB Security group
resource "aws_security_group" "lb" {
  name   = "${var.app_name}-${var.environment}-vpc-sg"
  vpc_id = aws_vpc.bars_vpc.id

  ingress {
    protocol    = "tcp"
    from_port   = 8080
    to_port     = 8080
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Traffic to the ECS Cluster should only come from the ALB
# or AWS services through an AWS PrivateLink
resource "aws_security_group" "ecs_tasks" {
  name   = "${var.app_name}-${var.environment}-ecs-sg"
  vpc_id = aws_vpc.bars_vpc.id

  ingress {
    protocol    = "tcp"
    from_port   = var.app_port
    to_port     = var.app_port
    cidr_blocks = [var.cidr]
  }

  ingress {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = [var.cidr]
  }

  egress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
    prefix_list_ids = [
      aws_vpc_endpoint.s3.prefix_list_id
    ]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.cidr]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}
