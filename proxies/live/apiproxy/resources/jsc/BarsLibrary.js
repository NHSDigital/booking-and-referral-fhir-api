/*
    LEGACY: BaRS proxy utility functions used by the S3-based routing path.
    TO BE REMOVED together with the LegacyS3Routing flow in bref-target.xml.

    This file should hold functions specific to this proxy.
    Use <IncludeURL>jsc://BarsLibrary.js</IncludeURL> to load it in a policy.
*/

function set_variables(location, vars) {
    // Unpacks a KVM JSON structure and publishes as context variables
    if (typeof vars !== 'object') { return; }
    for (var key in vars) {
        if (!vars.hasOwnProperty(key)) continue;
        variable = location + '.' + key;
        value = vars[key];
        if (typeof value === 'object' && value !== null) {
            set_variables(variable, value);
        } else {
            context.setVariable(variable, value);
        }
    }
}

function get_target_url_from_kvm_nhsd_target_identifier(system, value) {
    // Looks up target URL from the S3 routing table by system+value.
    // Returns null if not found.
    var NHSDTargetIdentifier = "NHSD-Target-Identifier"
    var b64decodedTarget = JSON.parse(context.getVariable("b64decodedTarget"));
    var url = b64decodedTarget[NHSDTargetIdentifier][system][value];
    if (url && url.endsWith('/')) {
        url = url.replace(/\/$/, "")
    }
    return url
}

function get_endpoint_from_pathsuffix(pathsuffix) {
    // Maps pathsuffix to endpoint name: meta, slots, appointment, serviceRequest, registry
    if (pathsuffix.includes('/meta'))           return 'meta'
    if (pathsuffix.includes('/Slots'))          return 'slots'
    if (pathsuffix.includes('/Appointment'))    return 'appointment'
    if (pathsuffix.includes('/ServiceRequest')) return 'serviceRequest'
    if (pathsuffix.includes('/registry'))       return 'registry'
    return null
}
