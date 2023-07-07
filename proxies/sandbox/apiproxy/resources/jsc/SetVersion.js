var acceptHeader = context.getVariable('request.header.Accept');
var versionRegex = /version=(1\.1\.0|1\.0\.0)/; //Matching if version number is either 1.0.0 OR 1.1.0
var versionMatch = acceptHeader.match(versionRegex);
if (versionMatch && versionMatch.length > 1) {
    var versionNumber = versionMatch[1];
    context.setVariable('versionNumber', versionNumber);
} else {
    context.setVariable('versionNumber', '1.0.0');
}