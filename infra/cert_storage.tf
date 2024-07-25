resource "aws_s3_bucket" "cert_storage" {
  bucket = "${local.name_prefix}-cert-storage"
}

locals {
  # NHSD cert file
  truststore_file_name = "nhs_truststore.pem"
}

data "aws_s3_object" "cert" {
  depends_on = [aws_s3_bucket.cert_storage]
  bucket = "${local.name_prefix}-cert-storage"
  key = local.truststore_file_name
}

output "cert" {
  value = data.aws_s3_object.cert.body
}
