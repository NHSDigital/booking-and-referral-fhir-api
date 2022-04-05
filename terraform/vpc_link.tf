# ECR
resource "aws_vpc_endpoint" "ecr_dkr" {
  vpc_id       = aws_vpc.bars_vpc.id
  service_name = "com.amazonaws.${var.region}.ecr.dkr"
  vpc_endpoint_type = "Interface"
  private_dns_enabled = true
  subnet_ids          = aws_subnet.private_subnets.*.id

  security_group_ids = [
    aws_security_group.ecs_tasks.id,
  ]

  tags = merge(local.tags, {Name = "${var.app_name}-${var.environment}-ecr"})
}

# CloudWatch
resource "aws_vpc_endpoint" "cloudwatch" {
  vpc_id       = aws_vpc.bars_vpc.id
  service_name = "com.amazonaws.${var.region}.logs"
  vpc_endpoint_type = "Interface"
  subnet_ids          = aws_subnet.private_subnets.*.id
  private_dns_enabled = true

  security_group_ids = [
    aws_security_group.ecs_tasks.id,
  ]

  tags = merge(local.tags, {Name = "${var.app_name}-${var.environment}-cloudwatch"})
}

# S3
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.bars_vpc.id
  service_name = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
#  route_table_ids = ["rtb-${var.app_name}${var.environment}"]

  tags = merge(local.tags, {Name = "${var.app_name}-${var.environment}-s3"})
}
