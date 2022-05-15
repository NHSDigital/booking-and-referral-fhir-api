# NOTE: mock-receiver is the same as sandbox

data "archive_file" "mock_receiver_archive" {
  type        = "zip"
  source_dir  = "${path.cwd}/../sandbox"
  output_path = "build/sandbox"
}

resource "null_resource" "mock-receiver_image_push" {
  triggers = {
    src_hash = data.archive_file.mock_receiver_archive.output_sha
  }

  provisioner "local-exec" {
    command = <<EOF
           make docker-push-sandbox
       EOF
  }
}

data "aws_ecr_image" "mock-receiver_image" {
  depends_on = [
    null_resource.mock-receiver_image_push
  ]
  repository_name = var.repository_name
  image_tag       = var.image_version
}
