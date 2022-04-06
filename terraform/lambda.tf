data "archive_file" "lambda_debug" {
  type        = "zip"
  #  source_dir = "../mock-receiver/debug"
  source_file = "../mock-receiver/debug/index.js"
  output_path = "build/index.zip"
}

resource "aws_lambda_function" "debug_endpoint_function" {
  function_name    = "${local.name_prefix}-debug"
  filename         = data.archive_file.lambda_debug.output_path
  handler          = "index.handler"
  source_code_hash = data.archive_file.lambda_debug.output_base64sha256
  runtime          = "nodejs14.x"
  role             = aws_iam_role.iam_for_lambda.arn
}
resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

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
