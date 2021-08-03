var queryParamaters = context.getVariable("request.querystring");
var serviceId = context.getVariable("request.header.service-id");
var kvmValue = "booking-and-referral-config.id." + serviceId
var url = context.getVariable(kvmValue)
context.setVariable("target.url", url + "?" + queryParamaters);
