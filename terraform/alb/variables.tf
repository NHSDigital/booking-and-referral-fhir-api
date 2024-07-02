data "aws_vpc" "bebop_vpc" {
  id = var.vpc_id
}
variable "name_prefix" {}
variable "short_prefix" {}
variable "vpc_id" {}
variable "private_subnet_ids" {
  type = list(string)
}
variable "container_port" {}
variable "listener_port" {}
variable "infra_private_subnet" {}
