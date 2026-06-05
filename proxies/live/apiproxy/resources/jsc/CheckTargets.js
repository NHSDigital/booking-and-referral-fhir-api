var b64decoded = JSON.parse(context.getVariable('b64decoded'));

if (b64decoded != null && b64decoded['system'] && b64decoded['value']) {
    context.setVariable('idMalformed', false);
} else {
    context.setVariable('idMalformed', true);
}
