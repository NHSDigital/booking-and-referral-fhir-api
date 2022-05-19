data "aws_subnet_ids" "this" {
    vpc_id = var.vpc_id

    tags = {
        Tier = "Public"
    }
}

resource "aws_lb" "network_load_balancer" {
    name               = "basic-load-balancer"
    load_balancer_type = "network"
    subnets            = data.aws_subnet_ids.this.ids

    enable_cross_zone_load_balancing = true

    tags = {
        Name = '${local.name_prefix}--network-load-balance'
    }
}

resource "aws_lb_listener" "nlb_listener" {
    for_each = var.nlb_ports

    load_balancer_arn = aws_lb.network_load_balancer.arn

    protocol = "TCP"
    port     = each.value

    default_action {
        type             = "forward"
        target_group_arn = aws_lb_target_group.this[each.key].arn
    }

    tags = {
        Name = '${local.name_prefix}--nlb-listener'
    }
}

resource "aws_lb_target_group" "this" {
    for_each = var.nlb_ports

    port     = each.value
    protocol = "TCP"
    vpc_id   = var.vpc_id

    stickiness = []

    depends_on = [
        aws_lb.network_load_balancer
    ]

    lifecycle {
        create_before_destroy = true
    }
}

resource "aws_autoscaling_attachment" "target" {
    for_each = var.nlb_ports

    autoscaling_group_name = var.autoscaling_group_name
    alb_target_group_arn   = aws_lb_target_group.this[each.value].arn
}

resource "aws_security_group" "nlb_security_group" {
    description = "Allow connection between NLB and target"
    vpc_id      = var.vpc_id
}

resource "aws_security_group_rule" "nlb_ingress_sg_rule" {
    for_each = var.nlb_ports

    security_group_id = aws_security_group.nlb_security_group.id
    from_port         = each.value
    to_port           = each.value
    protocol          = "tcp"
    type              = "ingress"
    cidr_blocks       = ["0.0.0.0/0"]
}
