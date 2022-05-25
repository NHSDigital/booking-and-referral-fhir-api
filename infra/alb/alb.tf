resource "aws_lb" "alb" {
  name               = var.name_prefix
  internal           = true
  load_balancer_type = "application"

  subnets         = var.public_subnet_ids
  security_groups = [aws_security_group.alb_security_group.id]
}

// TODO: narrow security
resource "aws_security_group" "alb_security_group" {
  name   = "${var.name_prefix}-alb"
  vpc_id = var.vpc_id

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "alb_arn" {
  value = aws_lb.alb.arn
}
