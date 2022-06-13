output "alb_target_group_arn" {
    value = aws_lb_target_group.http_mock_receiver_tg.arn
}

output "alb_listener_arn" {
    value = aws_lb_listener.api_http_80.arn
}

output "alb_arn" {
    value = aws_lb.alb.arn
}
