// Get context variables
var b64decoded = JSON.parse(context.getVariable("b64decoded"));
var pathSuffix = context.getVariable("proxy.pathsuffix")
var queryString = context.getVariable("request.querystring")
var isError = false;

var system = b64decoded.system
var value = b64decoded.value

// Get target url from KVM
var targetUrl = get_target_url_from_kvm(system, value)
if(targetUrl === null | system === null | value === null){
    isError = true
}
context.setVariable("isError", isError)

// Override target url
if(queryString !== ""){
    context.setVariable("target.url", targetUrl + pathSuffix + "?" + queryString);
}else{
    context.setVariable("target.url", targetUrl + pathSuffix);
}

