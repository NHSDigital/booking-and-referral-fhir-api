locals {
    vpc_cidr = data.aws_vpc.bebop_vpc.cidr_block
}

locals {
    name_prefix = "${var.project}-${var.environment}"
}

locals {
    private_subnet_cidr = [for subnet in local.private_subnet : subnet.cidr]
}

locals {
    private_subnet = [
        {
            cidr              = cidrsubnet(local.vpc_cidr, 8, 101)
            availability_zone = "eu-west-2a"
            is_public         = false
        }, {
            cidr              = cidrsubnet(local.vpc_cidr, 8, 102)
            availability_zone = "eu-west-2b"
            is_public         = false
        }, {
            cidr              = cidrsubnet(local.vpc_cidr, 8, 103)
            availability_zone = "eu-west-2c"
            is_public         = false
        }
    ]
}

variable "region" {
    default = "eu-west-2"
}

variable "project" {
    default = "bars-infra"
}

variable "domain_name" {
    default = "dev.api.platform.nhs.uk"
}

variable "environment" {
    default = "dev"
}


variable "service" {
    default = "infra"
}

variable "registries" {
    default = ["mock-receiver"]
}

variable "vpc_id" {
    default = "vpc-0d79f2b39f53e14f0"
}

variable "nlb_ports" {
    type    = map(number)
    default = {
        http  = 80
        https = 443
    }
}

variable "autoscaling_group_name" {
    default = "target-autoscaling-group"
}

variable "container_port" {
    default = 9000
}

variable "listener_port" {
    default = 80
}
