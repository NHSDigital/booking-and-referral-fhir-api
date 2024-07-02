
resource "aws_iam_role" lambda_role {
    name               = "${var.short_prefix}-${var.function_name}-role"
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


resource "aws_iam_role_policy" "lambda_role_policy" {
    name   = "${var.prefix}-${var.function_name}-policy"
    role   = aws_iam_role.lambda_role.id
    policy = var.policy_json
}