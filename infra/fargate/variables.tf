variable "region" {}
variable "vpc_id" {}

variable "name_prefix" {}

variable "subnets" {
  type = list(object({
    cidr              = string
    availability_zone = string
  }))
}
