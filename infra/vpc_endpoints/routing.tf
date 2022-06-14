resource "aws_route_table" "private_vpc_endpoint_rt" {
  vpc_id = var.vpc_id

  tags = {
    Name = "${var.name_prefix}-fargate"
  }
}

resource "aws_vpc_endpoint_route_table_association" "s3_vpc_endpoint_route_table" {
  route_table_id  = aws_route_table.private_vpc_endpoint_rt.id
  vpc_endpoint_id = aws_vpc_endpoint.s3.id
}

resource "aws_route_table_association" "private_route_table_assoc" {
  count = length(var.subnet_ids)

  route_table_id = aws_route_table.private_vpc_endpoint_rt.id
  subnet_id      = var.subnet_ids[count.index]
}
