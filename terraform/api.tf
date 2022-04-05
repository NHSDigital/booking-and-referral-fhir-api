resource "aws_api_gateway_rest_api" "main" {
  name = "${var.app_name}-${var.environment}-api"
  tags = local.tags
}

resource "aws_api_gateway_resource" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "debug"
}

resource "aws_api_gateway_method" "main" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.main.id
  http_method   = "ANY"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.proxy" = true
  }
}

/*
resource "aws_api_gateway_domain_name" "api_domain_name" {
  domain_name = "bars.${var.domain_name}"
  certificate_arn = aws_acm_certificate_validation.cert_validation_root.certificate_arn
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}
*/

resource "aws_api_gateway_integration" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.main.id
  http_method = aws_api_gateway_method.main.http_method

  request_parameters = {
    "integration.request.path.proxy" = "method.request.path.proxy"
  }

  type                    = "HTTP_PROXY"
  uri                     = "http://${aws_lb.nlb.dns_name}:${var.app_port}/{proxy}"
  integration_http_method = "GET"

  connection_type = "VPC_LINK"
  connection_id   = aws_api_gateway_vpc_link.this.id
}

resource "aws_api_gateway_deployment" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  stage_name  = "${var.environment}-env"
  depends_on  = [aws_api_gateway_integration.main]

  variables = {
    # just to trigger redeploy on resource changes
    resources = join(", ", [aws_api_gateway_resource.main.id])

    # note: redeployment might be required with other gateway changes.
    # when necessary run `terraform taint <this resource's address>`
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_vpc_link" "this" {
  name        = "${var.app_name}-vpc-link"
  target_arns = [aws_lb.nlb.arn]
}
