// Get context variables
var serviceId = context.getVariable("request.header.NHSD-Service");
var b64decoded = JSON.parse(context.getVariable("b64decoded"));
var pathSuffix = context.getVariable("proxy.pathsuffix")
var queryString = context.getVariable("request.querystring")
var isError = false;



// Get target url from KVM (NHSD-Target-Identifier header)
if(b64decoded != null){
    var system = b64decoded.system
    var value = b64decoded.value
    var targetUrl = get_target_url_from_kvm_nhsd_target_identifier(system, value)
    if(targetUrl === null | system === null | value === null){
        isError = true;
    }
}
else if(serviceId != null){
 // Get target url from KVM (NHSD-Service header)
    var targetUrl = get_target_url_from_kvm_nhsd_service(serviceId)
    if(targetUrl === null | serviceId === null){
        isError = true;
    }   
}


context.setVariable("isError", isError)

// Override target url
if(queryString !== ""){
    context.setVariable("target.url", targetUrl + pathSuffix + "?" + queryString);
}else{
    context.setVariable("target.url", targetUrl + pathSuffix);
}

