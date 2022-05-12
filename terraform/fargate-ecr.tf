resource "aws_ecr_repository" "bars-ecr-sandbox" {
  name = "${local.name_prefix}-ecr-sandbox"
}

resource "aws_ecr_repository_policy" "demo-repo-policy" {
  repository = aws_ecr_repository.bars-ecr-sandbox.name
  policy     = <<EOF
  {
    "Version": "2008-10-17",
    "Statement": [
      {
        "Sid": "adds full ecr access to the demo repository",
        "Effect": "Allow",
        "Principal": "*",
        "Action": [
          "ecr:BatchCheckLayerAvailability",
          "ecr:BatchGetImage",
          "ecr:CompleteLayerUpload",
          "ecr:GetDownloadUrlForLayer",
          "ecr:GetLifecyclePolicy",
          "ecr:InitiateLayerUpload",
          "ecr:PutImage",
          "ecr:UploadLayerPart"
        ]
      }
    ]
  }
  EOF
}

data "archive_file" "mock_receiver_sandbox_archive" {
  type        = "zip"
  source_dir  = "../sandbox"
  output_path = "build/sandbox"
}

resource "null_resource" "sandbox_image_push" {
  triggers = {
    src_hash = data.archive_file.mock_receiver_sandbox_archive.output_sha
  }

  provisioner "local-exec" {
    command = <<EOF
           make docker-push-sandbox
       EOF
  }
}

data "aws_ecr_image" "sandbox_image" {
  depends_on = [
    null_resource.sandbox_image_push
  ]
  repository_name = aws_ecr_repository.bars-ecr-sandbox.name
  image_tag       = "latest"
}

locals {
  sandbox_image = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com/${data.aws_ecr_image.sandbox_image.repository_name}:${data.aws_ecr_image.sandbox_image.image_tag}"
}
