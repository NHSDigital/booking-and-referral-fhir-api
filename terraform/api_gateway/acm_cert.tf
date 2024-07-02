resource "aws_acm_certificate" "service_certificate" {
    domain_name               = var.api_domain_name
    subject_alternative_names = []
    validation_method         = "DNS"

    lifecycle {
        create_before_destroy = true
    }
}

resource "aws_acm_certificate_validation" "service_certificate" {
    certificate_arn         = aws_acm_certificate.service_certificate.arn
    validation_record_fqdns = [for record in aws_route53_record.dns_validation : record.fqdn]
}

resource "aws_route53_record" "dns_validation" {
    for_each = {
        for dvo in aws_acm_certificate.service_certificate.domain_validation_options : dvo.domain_name => {
            name   = dvo.resource_record_name
            record = dvo.resource_record_value
            type   = dvo.resource_record_type
        }
    }

    allow_overwrite = true
    name            = each.value.name
    records         = [each.value.record]
    ttl             = 60
    type            = each.value.type
    zone_id         = var.zone_id
}