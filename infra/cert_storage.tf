resource "aws_s3_bucket" "cert_storage" {
  bucket = "${local.name_prefix}-cert-storage"
}