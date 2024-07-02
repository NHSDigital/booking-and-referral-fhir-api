module "subnets" {
  source      = "./subnet"
  name_prefix = local.name_prefix
  vpc_id      = var.vpc_id

  count  = length(local.public_subnet)
  subnet = local.public_subnet[count.index]
}

module "private_subnets" {
  source      = "./subnet"
  name_prefix = local.name_prefix
  vpc_id      = var.vpc_id

  count  = length(local.private_subnet)
  subnet = local.private_subnet[count.index]
}
