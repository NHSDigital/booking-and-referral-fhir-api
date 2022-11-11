// Get context variables
var b64decoded = JSON.parse(context.getVariable('b64decoded'))

// Check the structure of the TargetId
var idValid = (b64decoded != null && b64decoded['system'] && b64decoded['value'])
context.setVariable('idMalformed', !idValid)
