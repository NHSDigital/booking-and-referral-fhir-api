# ECR
resource "aws_vpc_endpoint" "ecr_dkr" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.${var.region}.ecr.dkr"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true
  subnet_ids          = aws_subnet.private_subnets.*.id
  security_group_ids  = [aws_security_group.vpc_endpoint_sg.id]

  tags = {
    Name = "${var.name_prefix}-ecr-dkr"
  }
}

resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.${var.region}.ecr.api"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true
  subnet_ids          = aws_subnet.private_subnets.*.id
  security_group_ids  = [aws_security_group.vpc_endpoint_sg.id]

  tags = {
    Name = "${var.name_prefix}-ecr-api"
  }
}

# CloudWatch
resource "aws_vpc_endpoint" "cloudwatch" {
  vpc_id             = var.vpc_id
  service_name       = "com.amazonaws.${var.region}.logs"
  vpc_endpoint_type  = "Interface"
  subnet_ids         = aws_subnet.private_subnets.*.id
  security_group_ids = [aws_security_group.vpc_endpoint_sg.id]

  tags = {
    Name = "${var.name_prefix}-cloudwatch"
  }
}

# S3
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private_vpc_endpoint_rt.id]

  tags = {
    Name = "${var.name_prefix}-s3"
  }
}
