var acceptHeader = context.getVariable('request.header.Accept');
var versionRegex = /version=([\w.-]+)/;
var versionMatch = acceptHeader.match(versionRegex);
if (versionMatch && versionMatch.length > 1) {
    var versionNumber = versionMatch[1].split('-')[0];
    context.setVariable('versionNumber', versionNumber);
} else {
    context.setVariable('versionNumber', '1.0.0');
}