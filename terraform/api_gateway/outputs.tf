output "service_domain_name" {
    value = aws_apigatewayv2_api_mapping.api_mapping.domain_name
}

output "api_execution_arn" {
    value = aws_apigatewayv2_api.service_api.execution_arn
}