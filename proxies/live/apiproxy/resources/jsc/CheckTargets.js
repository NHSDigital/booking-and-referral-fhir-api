// Get context variables
var serviceId = context.getVariable("request.header.NHSD-Service");
var b64decoded = JSON.parse(context.getVariable("b64decoded"));

var system = b64decoded.system
var value = b64decoded.value
var idNotFound = false;

// Get target url from KVM (NHSD-Target-Identifier header)
if(b64decoded != null){
    var targetUrl = get_target_url_from_kvm_nhsd_target_identifier(system, value)
    if(targetUrl === null | system === null | value === null){
        idNotFound = true;
    }
}

// Get target url from KVM (NHSD-Service header)
var targetUrl = get_target_url_from_kvm_nhsd_service(serviceId)
if(targetUrl === null | serviceId === null){
    idNotFound = true;
}

context.setVariable("idNotFound", idNotFound)
