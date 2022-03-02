// Get context variables
var b64decoded = JSON.parse(context.getVariable("b64decoded"));

var system = b64decoded.system
var value = b64decoded.value
var idNotFound = false;

// Get target url from KVM
var targetUrl = get_target_url_from_kvm(system, value)
if(targetUrl === null | system === null | value === null){
    idNotFound = true;
}
context.setVariable("idNotFound", idNotFound)
