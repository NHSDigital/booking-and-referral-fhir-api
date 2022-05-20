resource "aws_apigatewayv2_vpc_link" "alb_vpc_link" {
    name               = local.name_prefix
    security_group_ids = [aws_security_group.nlb_security_group.id]
    subnet_ids         = aws_subnet.public_subnets.*.id
}
