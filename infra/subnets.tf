resource "aws_subnet" "public_subnets" {
    count             = length(local.public_subnets)
    cidr_block        = local.public_subnets[count.index].cidr
    availability_zone = local.public_subnets[count.index].availability_zone
    vpc_id            = var.vpc_id

    tags = {
        Name = "${local.name_prefix}-private-${local.public_subnets[count.index].availability_zone}"
    }
}

locals {
    public_subnets = [
        {
            cidr              = cidrsubnet(local.vpc_cidr, 8, 111)
            availability_zone = "eu-west-2a"
        }, {
            cidr              = cidrsubnet(local.vpc_cidr, 8, 112)
            availability_zone = "eu-west-2b"
        }, {
            cidr              = cidrsubnet(local.vpc_cidr, 8, 113)
            availability_zone = "eu-west-2c"
        }
    ]
}
