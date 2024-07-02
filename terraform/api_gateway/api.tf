locals {
    api_stage_name = var.environment
}

resource "aws_apigatewayv2_api" "service_api" {
    name                         = "${var.prefix}-api"
    description                  = "Bars FHIR API - ${var.environment}"
    protocol_type                = "HTTP"
    disable_execute_api_endpoint = true
    body                         = var.oas
}

resource "aws_apigatewayv2_stage" "default" {
    depends_on  = [aws_cloudwatch_log_group.api_access_log]
    api_id      = aws_apigatewayv2_api.service_api.id
    name        = local.api_stage_name
    auto_deploy = true

  default_route_settings {
    logging_level          = "INFO"
    throttling_burst_limit = 100
    throttling_rate_limit  = 100
    detailed_metrics_enabled = true
  }
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_access_log.arn
    format          = "{ \"requestId\":\"$context.requestId\", \"extendedRequestId\":\"$context.extendedRequestId\", \"ip\": \"$context.identity.sourceIp\", \"caller\":\"$context.identity.caller\", \"user\":\"$context.identity.user\", \"requestTime\":\"$context.requestTime\", \"httpMethod\":\"$context.httpMethod\", \"resourcePath\":\"$context.resourcePath\", \"status\":\"$context.status\", \"protocol\":\"$context.protocol\",  \"responseLength\":\"$context.responseLength\", \"authorizerError\":\"$context.authorizer.error\", \"authorizerStatus\":\"$context.authorizer.status\", \"requestIsValid\":\"$context.authorizer.is_valid\"\"environment\":\"$context.authorizer.environment\" }"
  }

    # Bug in terraform-aws-provider with perpetual diff
    lifecycle {
        ignore_changes = [deployment_id]
    }
}

resource "aws_apigatewayv2_domain_name" "service_api_domain_name" {
    domain_name = var.api_domain_name
    domain_name_configuration {
        certificate_arn = aws_acm_certificate_validation.service_certificate.certificate_arn
        endpoint_type   = "REGIONAL"
        security_policy = "TLS_1_2"
    }
    mutual_tls_authentication {
    truststore_uri = "s3://${aws_s3_bucket.truststore_bucket.bucket}/${local.truststore_file_name}"
  }
    tags = {
        Name = "${var.prefix}-api-domain-name"
    }
}

resource "aws_apigatewayv2_api_mapping" "api_mapping" {
    api_id      = aws_apigatewayv2_api.service_api.id
    domain_name = aws_apigatewayv2_domain_name.service_api_domain_name.id
    stage       = aws_apigatewayv2_stage.default.id
}

resource "aws_route53_record" "api_domain" {
    zone_id = var.zone_id
    name    = aws_apigatewayv2_domain_name.service_api_domain_name.domain_name
    type    = "A"
    alias {
        evaluate_target_health = true
        name                   = aws_apigatewayv2_domain_name.service_api_domain_name.domain_name_configuration[0].target_domain_name
        zone_id                = aws_apigatewayv2_domain_name.service_api_domain_name.domain_name_configuration[0].hosted_zone_id
    }
}