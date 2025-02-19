// Get Accept header
var acceptHeader = context.getVariable('request.header.Accept') || "";
var acceptArray = acceptHeader.split(';');

// Default version if not found
var highestVersion = "1.0.0";

// Extract all versions from Accept header
var versions = [];

for (var i = 0; i < acceptArray.length; i++) {
    var acceptValue = acceptArray[i].trim();
    if (acceptValue.startsWith("version")) {
        var version = acceptValue.split('=')[1].trim();  // Trim spaces
        versions.push(version);
    }
}

// Function to convert version "X.Y.Z" to a comparable number (e.g., "1.2.0" → 1020)
function versionToNumber(version) {
    var parts = version.split('.').map(Number);
    if (parts.length !== 3 || parts.some(isNaN)) {
        return 0;  // Invalid version, ignore it
    }
    return parts[0] * 1000 + parts[1] * 10 + parts[2];
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
