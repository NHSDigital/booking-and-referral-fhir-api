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
  profile = "apim-dev"
  alias  = "acm_provider"
  region = "eu-west-2"
}

data "aws_caller_identity" "current" {}
