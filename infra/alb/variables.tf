variable "name_prefix" {}
variable "vpc_id" {}
variable "public_subnet_ids" {
  type = list(string)
}
