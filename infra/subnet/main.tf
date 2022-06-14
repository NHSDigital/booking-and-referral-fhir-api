variable "name_prefix" {}

variable "vpc_id" {}

variable "subnet" {
  type = object({
    cidr              = string,
    availability_zone = string,
    is_public         = bool,
  })
}

resource "aws_subnet" "subnet" {
  cidr_block              = var.subnet.cidr
  vpc_id                  = var.vpc_id
  availability_zone       = var.subnet.availability_zone
  map_public_ip_on_launch = var.subnet.is_public

  tags = {
    Name = "${var.name_prefix}-${var.subnet.is_public ? "public" : "private"}-${var.subnet.availability_zone}"
  }
}

output "subnet_id" {
  value = aws_subnet.subnet.id
}
