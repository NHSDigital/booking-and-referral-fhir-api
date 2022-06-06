resource "aws_apigatewayv2_api" "service_api" {
  name                         = "${local.name_prefix}-api"
  description                  = "BaRS mock-receiver service backend api - ${local.environment}"
  protocol_type                = "HTTP"
  disable_execute_api_endpoint = true
}

locals {
  # NHSD cert file
  truststore_file_name = "nhs_truststore.crt"
}
resource "aws_s3_bucket" "truststore_bucket" {
  bucket = "${local.name_prefix}-trustore"
}

resource "aws_s3_object" "upload_key_to_truststore" {
  bucket = aws_s3_bucket.truststore_bucket.bucket
  key    = local.truststore_file_name
  source = local.truststore_file_name
}

resource "aws_apigatewayv2_domain_name" "service_api_domain_name" {
  domain_name = local.service_domain_name

  domain_name_configuration {
    certificate_arn = aws_acm_certificate.service_certificate.arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }

  mutual_tls_authentication {
    truststore_uri = "s3://${aws_s3_bucket.truststore_bucket.bucket}/${aws_s3_object.upload_key_to_truststore.key}"
  }

  tags = {
    Name = "${local.name_prefix}-api-domain-name"
  }
}

resource "aws_apigatewayv2_api_mapping" "api_mapping" {
  api_id      = aws_apigatewayv2_api.service_api.id
  domain_name = aws_apigatewayv2_domain_name.service_api_domain_name.id
  stage       = aws_apigatewayv2_stage.default.id
}

locals {
  api_stage_name = local.environment
}

resource "aws_apigatewayv2_stage" "default" {
  depends_on  = [aws_cloudwatch_log_group.api_access_log]
  api_id      = aws_apigatewayv2_api.service_api.id
  name        = local.api_stage_name
  auto_deploy = true

  #  default_route_settings {
  #    logging_level = "OFF"
  #  }
  #  access_log_settings {
  #    destination_arn = aws_cloudwatch_log_group.api_access_log.arn
  #    format          ="{ \"requestId\":\"$context.requestId\", \"extendedRequestId\":\"$context.extendedRequestId\", \"ip\": \"$context.identity.sourceIp\", \"caller\":\"$context.identity.caller\", \"user\":\"$context.identity.user\", \"requestTime\":\"$context.requestTime\", \"httpMethod\":\"$context.httpMethod\", \"resourcePath\":\"$context.resourcePath\", \"status\":\"$context.status\", \"protocol\":\"$context.protocol\",  \"responseLength\":\"$context.responseLength\" }"
  #  }

  # Bug in terraform-aws-provider with perpetual diff
  lifecycle {
    ignore_changes = [deployment_id]
  }
}

resource "aws_cloudwatch_log_group" "api_access_log" {
  name              = "API-Gateway-Execution-Logs_${aws_apigatewayv2_api.service_api.id}/${local.api_stage_name}"
  retention_in_days = 7
}

resource "aws_apigatewayv2_route" "lambda_route" {
  api_id    = aws_apigatewayv2_api.service_api.id
  route_key = "ANY /${var.service}/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id             = aws_apigatewayv2_api.service_api.id
  integration_uri    = aws_lambda_function.mock_receiver_endpoint_function.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "root_route" {
  api_id    = aws_apigatewayv2_api.service_api.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.route_integration.id}"
}

resource "aws_apigatewayv2_integration" "route_integration" {
  api_id             = aws_apigatewayv2_api.service_api.id
  integration_uri    = local.alb_listener_arn
  integration_type   = "HTTP_PROXY"
  integration_method = "ANY"
  connection_type    = "VPC_LINK"
  connection_id      = local.vpc_link_id
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke-${local.environment}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.mock_receiver_endpoint_function.function_name
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_apigatewayv2_api.service_api.execution_arn}/*/*"
}

resource "aws_apigatewayv2_deployment" "deployment" {
  depends_on  = [aws_apigatewayv2_route.lambda_route, aws_apigatewayv2_integration.lambda_integration]
  api_id      = aws_apigatewayv2_api.service_api.id
  description = "BaRS api deployment"

  lifecycle {
    create_before_destroy = true
  }
}
