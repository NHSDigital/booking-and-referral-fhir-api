variable "app_name" {
    default = "bars3"
}
variable "environment" {
    default = "dev"
}
variable "aws_account_id" {
    description = "AWS account ID"
}

variable "aws_role_name" {
    description = "AWS role name"
}

locals {
    tags = {
        Project = var.app_name
        Environment = var.environment
    }
}

variable "app_port" {
    default = 5050
}

variable "bucket_name" {
    default = "test-bucket-bars"
}
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

variable "private_subnets_cidr" {
    description = "List of private subnets"
    default     = ["10.10.2.0/24", "10.10.3.0/24"]
}

variable "availability_zones" {
    description = "List of availability zones"
    default     = ["eu-west-2a", "eu-west-2b"]
}
