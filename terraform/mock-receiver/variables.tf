variable "region" {}

variable "name_prefix" {}

variable "vpc_id" {}
variable "cluster_id" {}

variable "image_version" {}
variable "container_port" {
  default = "9000"
}

variable "subnet_ids" {
  type = list(string)
}

data "aws_subnet" "private_subnets" {
  count = length(var.subnet_ids)
  id    = var.subnet_ids[count.index]
}

locals {
  service_name        = "mock-receiver"
  container_image_tag = "latest"
}
variable "alb_tg_arn" {
}
