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

variable "bucket_name" {
    default = "test-bucket-bars"
}
