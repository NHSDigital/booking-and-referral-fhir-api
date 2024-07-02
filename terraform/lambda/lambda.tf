module "lambda_function_container_image" {
    source = "terraform-aws-modules/lambda/aws"

    create_role = false
    lambda_role = aws_iam_role.lambda_role.arn
    function_name = "${var.short_prefix}_${var.function_name}"
    handler       = "${var.function_name}_handler.${var.function_name}_handler"

    create_package = false
    image_uri    = var.image_uri
    package_type = "Image"
    architectures = ["x86_64"]
    timeout = 6

    # A JWT encode took 7 seconds at default memory size of 128 and 0.8 seconds at 1024.
    # 2048 gets it down to around 0.5 but since Lambda is charged at GB * ms then it costs more for minimal benefit.
    memory_size = 1024

    environment_variables = var.environments
    image_config_command = ["${var.function_name}_handler.${var.function_name}_handler"]
}

resource "aws_cloudwatch_metric_alarm" "memory_alarm" {
    alarm_name                = "${var.short_prefix}_${var.function_name} memory alarm"
    comparison_operator       = "GreaterThanOrEqualToThreshold"
    evaluation_periods        = 1
    metric_name               = aws_cloudwatch_log_metric_filter.max_memory_used_metric.metric_transformation[0].name
    namespace                 = aws_cloudwatch_log_metric_filter.max_memory_used_metric.metric_transformation[0].namespace
    period                    = 600
    statistic                 = "Maximum"
    threshold                 = 256
    alarm_description         = "This metric monitors Lambda memory usage"
    insufficient_data_actions = []

}

resource "aws_cloudwatch_log_metric_filter" "max_memory_used_metric" {
    name           = "${var.short_prefix}_${var.function_name} max memory used"
    pattern        = "[type=REPORT, ...]"

    log_group_name = module.lambda_function_container_image.lambda_cloudwatch_log_group_name

    metric_transformation {
        name      = "max-memory-used"
        namespace = "${var.short_prefix}_${var.function_name}"
        value     = "$18"
    }
}