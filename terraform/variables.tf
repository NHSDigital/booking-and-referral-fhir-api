variable "project" {
  default = "bars"
}

variable "environment" {
  default = "dev"
}

variable "service" {
  default = "mock-receiver"
}

variable "domain_name" {
  default = "dev.api.platform.nhs.uk"
}

locals {
  name_prefix         = "${var.project}-${var.service}-${var.environment}"
  service_domain_name = "${var.environment}.${var.project}.${var.domain_name}"

  tags = {
    Project     = var.project
    Environment = var.environment
    Service     = var.service
  }
}
