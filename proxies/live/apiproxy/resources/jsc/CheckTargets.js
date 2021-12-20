// Get context variables
var serviceId = context.getVariable("request.header.NHSD-Service");
var idNotFound = false;

// Get target url from KVM
var targetUrl = get_target_url_from_kvm(serviceId)
if(targetUrl === null | serviceId === null){
    idNotFound = true;
}
context.setVariable("idNotFound", idNotFound)
