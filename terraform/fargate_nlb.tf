resource "aws_lb" "nlb" {
  name               = "${var.app_name}-${var.environment}-nlb"
  internal           = true
  load_balancer_type = "network"
  subnets            = aws_subnet.private_subnets.*.id

  enable_deletion_protection = false

  tags = local.tags
}

resource "aws_lb_target_group" "nlb_tg" {
  depends_on  = [
    aws_lb.nlb
  ]
  name        = "${var.app_name}-nlb-${var.environment}-tg"
  port        = var.app_port
  protocol    = "TCP"
  vpc_id      = aws_vpc.bars_vpc.id
  target_type = "ip"

  tags = local.tags
}

resource "aws_lb_listener" "nlb_listener" {
  load_balancer_arn = aws_lb.nlb.id
  port              = var.app_port
  protocol    = "TCP"

  default_action {
    target_group_arn = aws_lb_target_group.nlb_tg.id
    type             = "forward"
  }

  tags = local.tags
}
