/*
Monitoring Cluster: A cluster event will trigger a lambda which log the event to it's standard output. Then a cloudwatch
log will log that event
*/

resource "aws_cloudwatch_event_rule" "ecs_event_stream" {
  name        = "${var.name_prefix}-ecs-event-stream"
  description = "Passes ecs event logs to lambda that writes them to cw logs"

  event_pattern = <<PATTERN
  {
    "detail": {
      "clusterArn": ["${aws_ecs_cluster.fargate-cluster.arn}"]
    }
  }
PATTERN
}

resource "aws_cloudwatch_event_target" "ecs_event_stream" {
  rule = aws_cloudwatch_event_rule.ecs_event_stream.name
  arn  = aws_lambda_function.ecs_event_stream.arn
}

locals {
  lambda_file_name = "ecs_event_logger"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/${local.lambda_file_name}.js"
  output_path = "build/ecs_event_logger_lambda.zip"
}

resource "aws_lambda_permission" "ecs_event_stream" {
  statement_id  = "${var.name_prefix}_AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ecs_event_stream.arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ecs_event_stream.arn
}

resource "aws_lambda_function" "ecs_event_stream" {
  function_name    = "${var.name_prefix}-ecs-event-stream"
  role             = aws_iam_role.ecs_event_stream.arn
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  handler          = "${local.lambda_file_name}.handler"
  runtime          = "nodejs14.x"
}

resource "aws_lambda_alias" "ecs_event_stream" {
  name             = aws_lambda_function.ecs_event_stream.function_name
  description      = "latest"
  function_name    = aws_lambda_function.ecs_event_stream.function_name
  function_version = "$LATEST"
}

resource "aws_iam_role" "ecs_event_stream" {
  name = aws_cloudwatch_event_rule.ecs_event_stream.name

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs_event_stream" {
  role       = aws_iam_role.ecs_event_stream.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# FIXME: This dashboard is empty all the time!
# cloudwatch dashboard with logs insights query
resource "aws_cloudwatch_dashboard" "ecs-event-stream" {
  dashboard_name = "${var.name_prefix}-ecs-event-stream"

  dashboard_body = <<EOF
{
  "widgets": [
    {
      "type": "log",
      "x": 0,
      "y": 0,
      "width": 24,
      "height": 18,
      "properties": {
        "query": "SOURCE '/aws/lambda/${var.name_prefix}-ecs-event-stream' | fields @timestamp as time, detail.desiredStatus as desired, detail.lastStatus as latest, detail.stoppedReason as reason, detail.containers.0.reason as container_reason, detail.taskDefinitionArn as task_definition\n| filter @type != \"START\" and @type != \"END\" and @type != \"REPORT\"\n| sort detail.updatedAt desc, detail.version desc\n| limit 100",
        "region": "us-east-1",
        "title": "ECS Event Log"
      }
    }
  ]
}
EOF
}
