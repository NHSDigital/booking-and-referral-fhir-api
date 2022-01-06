resource "aws_s3_bucket" "test" {
  bucket = "${var.environment-name}-test-bucket"
  acl    = "private"
}