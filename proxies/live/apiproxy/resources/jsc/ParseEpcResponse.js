var statusCode = parseInt(context.getVariable("epcCalloutResponse.status.code"));

if (!statusCode || statusCode >= 500) {
    context.setVariable("epcUnavailable", true);
    return;
}
if (statusCode === 404) {
    context.setVariable("isError", true);
    return;
}

var body = context.getVariable("epcCalloutResponse.content");
var bundle;
try {
    bundle = JSON.parse(body);
} catch (e) {
    context.setVariable("epcInvalidResponse", true);
    return;
}

var entries = bundle.entry || [];
var address = null;
for (var i = 0; i < entries.length; i++) {
    var r = entries[i].resource;
    if (r && r.resourceType === "Endpoint" && r.status === "active" && r.address) {
        address = r.address.replace(/\/$/, "");
        break;
    }
}

if (!address) {
    context.setVariable("isError", true);
    return;
}

var pathSuffix = context.getVariable("proxy.pathsuffix") || "";
var qs = context.getVariable("request.querystring");
context.setVariable("target.url", address + pathSuffix + (qs ? "?" + qs : ""));
