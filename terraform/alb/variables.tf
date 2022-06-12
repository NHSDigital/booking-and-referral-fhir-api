data "aws_vpc" "bebop_vpc" {
  id = var.vpc_id
}
variable "name_prefix" {}
variable "vpc_id" {}
variable "public_subnet_ids" {
  type = list(string)
}
variable "container_port" {}
variable "listener_port" {}
variable "infra_private_subnet" {}
variable "infra_public_subnet" {}
