resource "aws_apigatewayv2_api" "service_api" {
  name                         = "${local.name_prefix}-api"
  description                  = "BaRS mock-receiver service backend api - ${local.environment}"
  protocol_type                = "HTTP"
  disable_execute_api_endpoint = true
}

locals {
  # NHSD cert file
  truststore_file_name = "truststore.crt"
}
resource "aws_s3_bucket" "truststore_bucket" {
  bucket = "${local.name_prefix}-trustore"
}
resource "aws_s3_bucket_versioning" "truststore_versioning" {
  bucket = aws_s3_bucket.truststore_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_object" "upload_key_to_truststore" {
  bucket = aws_s3_bucket_versioning.truststore_versioning.bucket
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

  // TODO: enable mtls
  #  mutual_tls_authentication {
  #    truststore_uri = "s3://${aws_s3_bucket.truststore_bucket.bucket}/${aws_s3_object.upload_key_to_truststore.key}"
  #  }

  tags = {
    Name = "${local.name_prefix}-api-domain-name"
  }
}

resource "aws_apigatewayv2_api_mapping" "api_mapping" {
  api_id      = aws_apigatewayv2_api.service_api.id
  domain_name = aws_apigatewayv2_domain_name.service_api_domain_name.id
  stage       = aws_apigatewayv2_stage.default.id
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.service_api.id
  name        = local.environment
  auto_deploy = true

  # Bug in terraform-aws-provider with perpetual diff
  lifecycle {
    ignore_changes = [deployment_id]
  }
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
    integration_uri  = local.alb_listener_arn
    integration_type = "HTTP_PROXY"
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
