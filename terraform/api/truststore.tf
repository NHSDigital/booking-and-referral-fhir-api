locals {
  # NHSD cert file
  truststore_file_name = "nhs_truststore.pem"
}

resource "aws_s3_bucket" "truststore_bucket" {
  bucket = "${var.name_prefix}-truststore"
}

resource "aws_s3_object_copy" "copy_cert_from_infra" {
  bucket = aws_s3_bucket.truststore_bucket.bucket
  key    = local.truststore_file_name
  source = "${var.cert_storage_bucket}/${local.truststore_file_name}"
}
