resource "aws_apigatewayv2_api" "service_api" {
  name          = "${local.name_prefix}-api"
  description   = "BaRS mock-receiver service backend api - ${var.environment}"
  protocol_type = "HTTP"
  body          = templatefile("api.yaml", {})

}

resource "aws_apigatewayv2_domain_name" "service_api_domain_name" {
  domain_name = local.service_domain_name

  domain_name_configuration {
    certificate_arn = aws_acm_certificate.service_certificate.arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }

  /*
    dynamic "mutual_tls_authentication" {
      for_each = length(keys(var.mutual_tls_authentication)) == 0 ? [] : [var.mutual_tls_authentication]

      content {
        truststore_uri     = mutual_tls_authentication.value.truststore_uri
        truststore_version = try(mutual_tls_authentication.value.truststore_version, null)
      }
    }

  */
  tags = {
    Name = "${local.name_prefix}-api-domain-name"
  }
}

resource "aws_apigatewayv2_api_mapping" "example" {
  api_id      = aws_apigatewayv2_api.service_api.id
  domain_name = aws_apigatewayv2_domain_name.service_api_domain_name.id
  stage       = aws_apigatewayv2_stage.default.id
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.service_api.id
  name        = var.environment
  auto_deploy = true

  # Bug in terraform-aws-provider with perpetual diff
  lifecycle {
    ignore_changes = [deployment_id]
  }
}

resource "aws_apigatewayv2_route" "this" {
  api_id    = aws_apigatewayv2_api.service_api.id
  route_key = "ANY /${var.service}/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.route.id}"

  #  api_key_required                    = try(each.value.api_key_required, null)
  #  authorization_type                  = try(each.value.authorization_type, "NONE")
  #  authorizer_id                       = try(aws_apigatewayv2_authorizer.this[each.value.authorizer_key].id, each.value.authorizer_id, null)
  #  model_selection_expression          = try(each.value.model_selection_expression, null)
  #  operation_name                      = try(each.value.operation_name, null)
  #  route_response_selection_expression = try(each.value.route_response_selection_expression, null)
  #  target                              = "integrations/${aws_apigatewayv2_integration.this[each.key].id}"
  #
  # Not sure what structure is allowed for these arguments...
  #  authorization_scopes = try(each.value.authorization_scopes, null)
  #  request_models  = try(each.value.request_models, null)
}

resource "aws_apigatewayv2_integration" "route" {
  api_id             = aws_apigatewayv2_api.service_api.id
  integration_uri    = aws_lambda_function.mock_receiver_endpoint_function.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.mock_receiver_endpoint_function.function_name
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_apigatewayv2_api.service_api.execution_arn}/*/*"
}

resource "aws_apigatewayv2_deployment" "deployment" {
  depends_on  = [aws_apigatewayv2_integration.route]
  api_id      = aws_apigatewayv2_api.service_api.id
  description = "BaRS api deployment"

  lifecycle {
    create_before_destroy = true
  }
}
