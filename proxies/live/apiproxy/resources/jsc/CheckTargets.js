// Get context variables
var b64decoded = JSON.parse(context.getVariable('b64decoded'))

// Check the structure of the TargetId
if (b64decoded != null && b64decoded['system'] && b64decoded['value']) {
  var idNotFound = false

// Get target url from KVM (NHSD-Target-Identifier header)
  var system = b64decoded.system
  var value = b64decoded.value
  var targetUrl = get_target_url_from_kvm_nhsd_target_identifier(system, value)
  if (targetUrl === null) {
    idNotFound = true
  }

  context.setVariable('idNotFound', idNotFound)

} else {
  context.setVariable('idMalformed', true)
}
