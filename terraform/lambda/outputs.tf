output "function_name" {
    value = module.lambda_function_container_image.lambda_function_name
}
output "lambda_arn" {
    value = module.lambda_function_container_image.lambda_function_arn
}
output "invoke_arn" {
    value = module.lambda_function_container_image.lambda_function_invoke_arn
}