
function get_url(serviceId, endpoint) {
  /*
    Get a url value from the booking-and-referral kvm.
    the valid endpoints at the moment are:
    - meta
    - slots
    
    If there is no value in the kvm it returns null
  */
    var location = "booking-and-referral-config.NHSD-ServiceIdentifier." + serviceId + endpoint;
    var url = context.getVariable(location);
    return url
}

//////////////////////////////////
// Geting context variables...
//////////////////////////////////

var queryParamaters = context.getVariable("request.querystring");
var serviceId = context.getVariable("request.header.NHSD-ServiceIdentifier");
var endpoint = context.getVariable("proxy.pathsuffix")

var isError = false;

var targetUrl = get_url(serviceId,endpoint)

if(url === null | serviceId === null){
    isError = true
}

context.setVariable("isError", isError)
context.setVariable("target.url", targetUrl + "?" + queryParamaters);

