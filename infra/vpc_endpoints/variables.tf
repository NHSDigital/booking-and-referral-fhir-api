variable "name_prefix" {}

variable "region" {
  default = "eu-west-2"
}

variable "vpc_id" {}
variable "subnet_ids" {
  type = list(string)
}
