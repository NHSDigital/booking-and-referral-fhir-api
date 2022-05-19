variable "region" {
  default = "eu-west-2"
}

variable "project" {
  default = "bars-infra"
}

variable "domain_name" {
  default = "dev.api.platform.nhs.uk"
}

variable "environment" {
  default = "dev"
}

variable "service" {
  default = "infra"
}
locals {
  name_prefix = "${var.project}-${var.environment}"
}

variable "registries" {
  default = ["mock-receiver"]
}

variable "vpc_id" {
  default = "vpc-0d79f2b39f53e14f0"
}
