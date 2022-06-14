data "aws_route53_zone" "zone" {
  name = var.domain_name
}

module "api" {
  source = "./api"

  name_prefix     = local.name_prefix
  zone_id         = data.aws_route53_zone.zone.id
  api_domain_name = local.service_domain_name
  environment     = local.environment
  lb              = {
    listener_arn = module.alb.alb_listener_arn
    vpc_link_id  = local.vpc_link_id
  }
}
