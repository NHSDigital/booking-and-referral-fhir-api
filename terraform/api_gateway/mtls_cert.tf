locals {
  # NHSD cert file
  truststore_file_name = "server-cert.pem"
}

data "aws_s3_bucket" "cert_storage" {
  bucket = "bars-dev-cert-storage"
}

data "aws_s3_object" "cert" {
  bucket = data.aws_s3_bucket.cert_storage.bucket
  key = local.truststore_file_name
}

resource "aws_s3_bucket" "truststore_bucket" {
  bucket = "${var.prefix}-truststore"
  force_destroy = true
}

resource "aws_s3_object_copy" "copy_cert_from_storage" {
  bucket = aws_s3_bucket.truststore_bucket.bucket
  key    = local.truststore_file_name
  source ="${data.aws_s3_object.cert.bucket}/${local.truststore_file_name}"
}