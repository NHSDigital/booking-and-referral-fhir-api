
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

