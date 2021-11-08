// Get context variables
var serviceId = context.getVariable("request.header.NHSD-Service");

var requestPath = context.getVariable("request.path")
var prNumber = context.getVariable("PR_LABEL")


// Get target url from KVM
var targetUrl = get_target_url_from_kvm(serviceId)
if(targetUrl === null | serviceId === null){
    isError = true
}
context.setVariable("isError", isError)

// Override target url
if(requestPath.includes("pr")){
    context.setVariable("target.url", "https://internal-dev.api.service.nhs.uk/bars-mock-receiver-proxy-"+ prNumber);
}

