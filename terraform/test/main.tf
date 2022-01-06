provider aws {
  region  = "eu-west-2"
  profile = var.aws-profile
}

module "s3" {}
