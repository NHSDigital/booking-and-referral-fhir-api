data "aws_lb" "alb" {
  arn = local.alb_arn
}

resource "aws_lb_listener" "api_http_80" {
  load_balancer_arn = data.aws_lb.alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = module.mock-receiver.target_group_arn
  }
}

// TODO: Currently not used. Maybe create one endpoint for testing if ALB is working when ECS is not. Similar to /_ping
resource "aws_lb_listener" "fixed_response" {
  load_balancer_arn = local.alb_arn
  port              = "81"
  protocol          = "HTTP"


  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "Hello from alb -> fixed response"
      status_code  = "200"
    }
  }
}

