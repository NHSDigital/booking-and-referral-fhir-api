terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4"
    }
  }
  backend "s3" {
    bucket = "nhsd-apim-bars-min-terraform"
    region = "eu-west-2"
    #    profile = "apim-dev"
    #    shared_credentials_file = "~/.aws/credentials"

  }
}

provider "aws" {
  region  = "eu-west-2"
  profile = "apim-dev"
  default_tags {
    tags = {
      Project     = var.project
      Environment = local.environment
      Service     = var.service
    }
  }
}

provider "aws" {
  alias  = "acm_provider"
  region = "eu-west-2"
}
data "aws_caller_identity" "current" {}

data "terraform_remote_state" "bebop-infra" {
  backend = "s3"
  config = {
    bucket = "terraform-nhsd-apim-bebop-infra"
    key    = "infra"
    region = "eu-west-2"
  }
}
