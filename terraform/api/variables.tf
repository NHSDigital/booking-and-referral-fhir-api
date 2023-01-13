variable "name_prefix" {}
variable "environment" {}
variable "zone_id" {}
variable "api_domain_name" {}
variable "cert_storage_bucket" {}
variable "lb" {
  type = object({
    vpc_link_id  = string,
    listener_arn = string
  })
}
