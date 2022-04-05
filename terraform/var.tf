variable "region" {
  default = "eu-west-2"
}
variable "environment" {
  default = "dev"
}

variable "domain_name" {
  default = "dev.api.platform.nhs.uk"
}

variable "project" {
  default = "bars"
}

variable "app_name" {
  default = "bars3"
}

locals {
  tags = {
    App         = var.app_name
    Project     = var.project
    Environment = var.environment
  }
}

variable "app_port" {
  default = 5050
}

# Networking
variable "cidr" {
  description = "The CIDR block for the VPC."
  default     = "10.10.0.0/16"
}

variable "public_subnets" {
  description = "List of public subnets"
  default     = ["10.10.100.0/24", "10.10.101.0/24"]
}

variable "private_subnets" {
  description = "List of private subnets"
  default     = ["10.10.0.0/24", "10.10.1.0/24"]
}

variable "availability_zones" {
  description = "List of availability zones"
  default     = ["eu-west-2a", "eu-west-2b"]
}
