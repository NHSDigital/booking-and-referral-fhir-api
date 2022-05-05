resource "aws_ecr_repository" "bars-ecr-sandbox" {
  name = "${local.name_prefix}-ecr-sandbox"
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
