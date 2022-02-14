resource "aws_s3_bucket" "test-bucket-bars" {
    bucket = "${var.bucket_name}" 
    acl = "${var.acl_value}"   
}