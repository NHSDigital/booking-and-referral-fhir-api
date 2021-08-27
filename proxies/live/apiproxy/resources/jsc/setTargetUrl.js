
function get_target_url_from_kvm(serviceId, endpoint) {
  /*
    Get a url value from the booking-and-referral kvm.
    the valid endpoints at the moment are:
    - meta
    - slots
    
    If there is no value in the kvm it returns null
  */
    var location = "booking-and-referral-config.NHSD-ServiceIdentifier." + serviceId + "." + endpoint;
    var url = context.getVariable(location);
    return url
}

function get_endpoint_from_pathsuffix(pathsuffix) {
  /*
    Get a the endpoint  value from the pathsuffix.
    the valid endpoints at the moment are:
    - meta
    - Slots
    - Appointment
    - ServiceRequest
    - registry
    
    If there is no match in the pathsuffix returns null
  */
    if (pathsuffix.includes('/meta')) {
      return 'meta'
    }
    if (pathsuffix.includes('/Slots')) {
      return 'Slots'
    }
    if (pathsuffix.includes('/Appointment')) {
      return 'Appointment'
    }
    if (pathsuffix.includes('/ServiceRequest')) {
      return 'ServiceRequest'
    }
    if (pathsuffix.includes('/registry')) {
      return 'registry'
    }
    return null
}

var serviceId = context.getVariable("request.header.NHSD-ServiceIdentifier");
var pathSuffix = context.getVariable("proxy.pathsuffix")
var isError = false;

var endpoint = get_endpoint_from_pathsuffix(pathSuffix)
var targetUrl = get_target_url_from_kvm(serviceId,endpoint)

if(targetUrl === null | serviceId === null){
    isError = true
}

context.setVariable("isError", isError)
context.setVariable("target.url", targetUrl);

