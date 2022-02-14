terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider aws {
  region  = "eu-west-2"
  profile = "${AWS_PROFILE}"
}

module "s3" {
    source = "test"      
}
