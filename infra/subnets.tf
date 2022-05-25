locals {
    public_subnets = [
        {
            cidr              = cidrsubnet(local.vpc_cidr, 8, 111)
            availability_zone = "eu-west-2a"
            is_public         = true
        }, {
            cidr              = cidrsubnet(local.vpc_cidr, 8, 112)
            availability_zone = "eu-west-2b"
            is_public         = true
        }, {
            cidr              = cidrsubnet(local.vpc_cidr, 8, 113)
            availability_zone = "eu-west-2c"
            is_public         = true
        }
    ]
}

module "subnets" {
    source      = "./subnet"
    name_prefix = local.name_prefix
    vpc_id      = var.vpc_id

    count  = length(local.public_subnets)
    subnet = local.public_subnets[count.index]
}
