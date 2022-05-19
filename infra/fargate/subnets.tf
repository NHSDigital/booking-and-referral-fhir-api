resource "aws_subnet" "private_subnets" {
  count             = length(var.subnets)
  cidr_block        = var.subnets[count.index].cidr
  availability_zone = var.subnets[count.index].availability_zone
  vpc_id            = var.vpc_id

  tags = {
    Name = "${var.name_prefix}-private-${var.subnets[count.index].availability_zone}"
  }
}
