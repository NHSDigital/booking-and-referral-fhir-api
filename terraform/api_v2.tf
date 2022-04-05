resource "aws_apigatewayv2_api" "bars_api" {
  name          = "${var.app_name}-${var.environment}-api-v2"
  description   = "BaRS API"
  protocol_type = "HTTP"
  body          = templatefile("api.yaml", { nlb_dns = "http://${aws_lb.nlb.dns_name}:${var.app_port}/debug" })

  tags = merge(local.tags, { Name = "${var.app_name}-api" })
}

/*
resource "aws_apigatewayv2_domain_name" "bars_api_domain_name" {
  domain_name              = "bars-v2.${var.domain_name}"

  domain_name_configuration {
    certificate_arn = aws_acm_certificate.bars_certificate.arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }

  dynamic "mutual_tls_authentication" {
    for_each = length(keys(var.mutual_tls_authentication)) == 0 ? [] : [var.mutual_tls_authentication]

    content {
      truststore_uri     = mutual_tls_authentication.value.truststore_uri
      truststore_version = try(mutual_tls_authentication.value.truststore_version, null)
    }
  }

  tags = merge(local.tags, {Name = "${var.app_name}-${var.environment}-api"})
}

*/
