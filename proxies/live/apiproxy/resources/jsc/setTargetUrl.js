var queryParamaters = context.getVariable("request.querystring");
var serviceId = context.getVariable("request.header.service-id");
var kvmValue = "booking-and-referral-config.id." + serviceId;
var url = context.getVariable(kvmValue);
var isError = false;

if(url === null | serviceId === null){
    isError = true
}

context.setVariable("isError", isError)
context.setVariable("target.url", url + "?" + queryParamaters);
