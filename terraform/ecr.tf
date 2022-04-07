resource "aws_ecr_repository" "bars-ecr-repository" {
  name = "${local.name_prefix}-ecr-repo"
  tags = local.tags
}

data "archive_file" "mock_receiver_archive" {
  type        = "zip"
  source_dir  = "../sandbox"
  output_path = "build/mock-receiver"
}

resource "null_resource" "image_push" {
  triggers = {
    src_hash = data.archive_file.mock_receiver_archive.output_sha
  }

  provisioner "local-exec" {
    command = <<EOF
           make docker-push
       EOF
  }
}
data aws_ecr_image lambda_image {
  depends_on = [
    null_resource.image_push
  ]
  repository_name = aws_ecr_repository.bars-ecr-repository.name
  image_tag       = "latest"
}
