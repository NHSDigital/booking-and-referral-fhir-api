locals {
  # NHSD cert file
  truststore_file_name = "nhs_truststore.crt"
}

data "aws_s3_object" "cert" {
  bucket = var.cert_storage_bucket 
  key = local.truststore_file_name
}

resource "aws_s3_bucket" "truststore_bucket" {
  bucket = "${var.name_prefix}-truststore"
}

resource "aws_s3_object" "upload_key_to_truststore" {
  bucket = aws_s3_bucket.truststore_bucket.bucket
  key    = local.truststore_file_name
  source = data.aws_s3_object.cert.body
}
