// Get context variables
var b64decoded = JSON.parse(context.getVariable('b64decoded'))

// Check the structure of the TargetId
var isSchemaValid = (b64decoded != null && b64decoded['system'] && b64decoded['value'])
context.setVariable('idMalformed', !isSchemaValid)

// Check the value
var isValueValid = b64decoded.system === "tests" && b64decoded.value.startsWith("NHS")
context.setVariable('isError', !isValueValid)
