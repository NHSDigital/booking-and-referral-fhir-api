resource "aws_alb" "bars_application_load_balancer" {
  name               = "${var.app_name}-${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = aws_subnet.public_subnets.*.id
  security_groups    = [aws_security_group.alb_security_group.id]

  tags = local.tags
}
resource "aws_security_group" "alb_security_group" {
  vpc_id = aws_vpc.bars_vpc.id

  ingress {
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = merge(local.tags, { Name = "${var.app_name}-${var.environment}-alb-sg" })
}

resource "aws_lb_target_group" "alb_target_group" {
  name        = "${var.app_name}-${var.environment}-alb-tg"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.bars_vpc.id

  health_check {
    healthy_threshold   = "3"
    interval            = "300"
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = "3"
    path                = "/v1/status"
    unhealthy_threshold = "2"
  }

  tags = local.tags
}

resource "aws_lb_listener" "alb_listener" {
  load_balancer_arn = aws_alb.bars_application_load_balancer.id
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.alb_target_group.id
  }
  tags = merge(local.tags, { Name = "${var.app_name}-${var.environment}-alb-listener" })
}
