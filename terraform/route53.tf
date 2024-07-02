locals {
  zone_subdomain = var.project_short_name
}

data "aws_route53_zone" "root_zone" {
  name = var.root_domain_name
}

locals {
  project_zone_name = "${local.zone_subdomain}.${data.aws_route53_zone.root_zone.name}"
}

data "aws_route53_zone" "project_zone" {
  name    = local.project_zone_name
}