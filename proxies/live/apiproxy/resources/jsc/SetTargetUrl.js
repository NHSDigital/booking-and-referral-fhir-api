// Get context variables
var serviceId = context.getVariable("request.header.NHSD-ServiceIdentifier");
var pathSuffix = context.getVariable("proxy.pathsuffix")
var queryString = context.getVariable("request.querystring")
var isError = false;

// Get target url from KVM
var targetUrl = get_target_url_from_kvm(serviceId)
if(targetUrl === null | serviceId === null){
    isError = true
}
context.setVariable("isError", isError)

// Override target url
if(queryString !== ""){
    context.setVariable("target.url", targetUrl + pathSuffix + "?" + queryString);
}else{
    context.setVariable("target.url", targetUrl + pathSuffix);
}

