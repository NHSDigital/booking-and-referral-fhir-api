
locals {
    lambda_dir    = abspath("${path.root}/../backend")
    source_path   = local.lambda_dir
    path_include  = ["**"]
    path_exclude  = ["**/__pycache__/**"]
    files_include = setunion([for f in local.path_include : fileset(local.source_path, f)]...)
    files_exclude = setunion([for f in local.path_exclude : fileset(local.source_path, f)]...)
    files         = sort(setsubtract(local.files_include, local.files_exclude))

    dir_sha = sha1(join("", [for f in local.files : filesha1("${local.source_path}/${f}")]))
}

#resource "docker_image" "lambda_function_docker" {
module "docker_image" {
    source = "terraform-aws-modules/lambda/aws//modules/docker-build"

    create_ecr_repo = true
    ecr_repo        = "${local.prefix}-lambda-repo"
    docker_file_path = "lambda.Dockerfile"
    ecr_repo_lifecycle_policy = jsonencode({
        "rules" : [
            {
                "rulePriority" : 1,
                "description" : "Keep only the last 2 images",
                "selection" : {
                    "tagStatus" : "any",
                    "countType" : "imageCountMoreThan",
                    "countNumber" : 2
                },
                "action" : {
                    "type" : "expire"
                }
            }
        ]
    })

    platform = "linux/amd64"
    use_image_tag = false
    source_path   = local.lambda_dir
    triggers = {
        dir_sha = local.dir_sha
    }
}
