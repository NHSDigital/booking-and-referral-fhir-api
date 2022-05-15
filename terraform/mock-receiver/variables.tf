variable "name_prefix" {}

variable "vpc_id" {}
variable "cluster_id" {}

variable "repository_url" {}
variable "repository_name" {}
variable "image_version" {}
variable "container_port" {
  default = "9000"
}

variable "subnet_ids" {
  type = list(string)
}
