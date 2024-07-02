variable "project_name" {
    default = "bars"
}

variable "project_short_name" {
    default = "bars"
}

variable "service" {
    default = "fhir-api"
}
data "aws_vpc" "default" {
    default = true
}
data "aws_subnets" "default" {
    filter {
        name   = "vpc-id"
        values = [data.aws_vpc.default.id]
    }
}

locals {
    root_domain = "dev.api.platform.nhs.uk"
}

locals {
    project_domain_name = data.aws_route53_zone.project_zone.name
}

locals {
    environment         = terraform.workspace
    prefix              = "${var.project_name}-${var.service}-${local.environment}"
    short_prefix        = "${var.project_short_name}-${local.environment}"
    service_domain_name = "${local.environment}.${local.project_domain_name}"

    tags = {
        Project     = var.project_name
        Environment = local.environment
        Service     = var.service
    }
}

variable "region" {
    default = "eu-west-2"
}

variable "root_domain_name" {
    default = "dev.api.platform.nhs.uk"
}