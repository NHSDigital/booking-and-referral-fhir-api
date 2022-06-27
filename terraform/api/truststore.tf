locals {
  # NHSD cert file
  truststore_file_name = "nhs_truststore.crt"
}

resource "aws_s3_bucket" "truststore_bucket" {
  bucket = "${var.name_prefix}-trustore"
}

resource "aws_s3_object" "upload_key_to_truststore" {
  bucket = aws_s3_bucket.truststore_bucket.bucket
  key    = local.truststore_file_name
  source = local.truststore_file_name
}
