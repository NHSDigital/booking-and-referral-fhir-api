// LEGACY: Resolve target URL from the S3 routing table (b64decodedTarget).
// TO BE REMOVED together with the LegacyS3Routing flow in bref-target.xml.

var b64decoded = JSON.parse(context.getVariable("b64decoded"));
var pathSuffix = context.getVariable("proxy.pathsuffix")
var queryString = context.getVariable("request.querystring")
var isError = false;

if (b64decoded != null) {
    var system = b64decoded.system
    var value = b64decoded.value
    var targetUrl = get_target_url_from_kvm_nhsd_target_identifier(system, value)
    if (targetUrl === null || targetUrl === undefined || system === null || value === null) {
        isError = true;
    }
}

context.setVariable("isError", isError)

if (queryString !== "") {
    context.setVariable("target.url", targetUrl + pathSuffix + "?" + queryString);
} else {
    context.setVariable("target.url", targetUrl + pathSuffix);
}
