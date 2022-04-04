terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3"
    }
  }
  backend "s3" {
    bucket = "nhsd-apim-bars-terraform"
    region = "eu-west-2"
  }
}

provider "aws" {
  region  = "eu-west-2"
}

provider "aws" {
  alias  = "acm_provider"
  region = "eu-west-2"
}
