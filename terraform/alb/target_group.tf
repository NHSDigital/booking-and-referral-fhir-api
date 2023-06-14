resource "aws_lb_target_group" "http_mock_receiver_tg" {
  name        = var.short_prefix
  port        = var.container_port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    path = "/_status"
  }
}
