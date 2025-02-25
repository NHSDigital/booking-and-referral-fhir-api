// Get Accept header
var acceptHeader = context.getVariable('request.header.Accept') || "";
var acceptArray = acceptHeader.split(',');

// Default version if not found
var highestVersion = "1.0.0";

// Extract all versions from Accept header
var versions = [];

for (var i = 0; i < acceptArray.length; i++) {
    var acceptValue = acceptArray[i].trim();
    var params = acceptValue.split(';');
    for (var j = 0; j < params.length; j++) {
        var param = params[j].trim().toLowerCase();  // Convert to lowercase
        if (param.startsWith("version")) {
            var version = param.split('=')[1].trim();  // Trim spaces
            versions.push(version);
        }
    }
}

// Function to convert version "X.Y.Z" to a comparable number (e.g., "1.2.0" → 10200)
function versionToNumber(version) {
    var parts = version.split('.').map(Number);
    if (parts.length !== 3 || parts.some(isNaN)) {
        return 0;  // Invalid version, ignore it
    }
    return parts[0] * 10000 + parts[1] * 100 + parts[2];
}

// Find the highest version
if (versions.length > 0) {
    highestVersion = versions.reduce((max, current) =>
        versionToNumber(current) > versionToNumber(max) ? current : max,
        "1.0.0"
    );
}

// Store values in Apigee variables
context.setVariable('versionNumber', highestVersion);
context.setVariable('versionNumberNumeric', versionToNumber(highestVersion));
