# NOTE: mock-receiver is the same as sandbox

locals {
  mock_receiver_path = "${path.cwd}/../sandbox"
  specification_path = "${path.cwd}/../specification"
}

data "archive_file" "mock_receiver_archive" {
  type        = "zip"
  source_dir  = local.mock_receiver_path
  output_path = "build/sandbox.zip"
}

data "archive_file" "specification_archive" {
  type        = "zip"
  source_dir  = local.specification_path
  output_path = "build/specification.zip"
}

data "aws_caller_identity" "current" {}

resource "null_resource" "mock-receiver_image_push" {
  depends_on = [aws_ecr_repository.mock_receiver_registry]
  triggers   = {
    src_hash = data.archive_file.mock_receiver_archive.output_sha
    specification_src = data.archive_file.specification_archive.output_sha
  }

  provisioner "local-exec" {
    interpreter = ["bash", "-c"]
    command = <<EOF
    export AWS_PROFILE=apim-dev
    aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin ${data.aws_caller_identity.current.account_id}.dkr.ecr.eu-west-2.amazonaws.com
    ecr_url=${aws_ecr_repository.mock_receiver_registry.repository_url}
    image_tag=$ecr_url:latest
    docker build --platform linux/amd64 -t $image_tag -f ${local.mock_receiver_path}/Dockerfile ${local.mock_receiver_path}
    docker push -a $ecr_url
    aws ecs update-service --cluster ${var.name_prefix} --service ${var.name_prefix} --force-new-deployment --region eu-west-2
    sleep 50
    counter=0
    while [ $counter -lt 8 ]
    do
      echo "Waiting for Service to be up and running..."
        ((counter=counter+1))
        echo $counter
        sleep 80
      fi
    done  
    
    EOF
  }
}
