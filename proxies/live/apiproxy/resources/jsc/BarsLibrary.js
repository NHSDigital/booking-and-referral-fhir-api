/*
    This file should hold functions specific to this proxy.
    This way we can share functions between javascript policies.
    In order to load this library in your javascript policy
    use the tag <IncludeURL>jsc://BarsLibrary.js</IncludeURL>
    for reference see:
    https://www.googlecloudcommunity.com/gc/Apigee/Can-you-include-a-Javascript-in-another-Javascript/m-p/59862#M51664

*/

function get_endpoint_from_pathsuffix(pathsuffix) {
/*
    Get a the endpoint  value from the pathsuffix.
    the valid endpoints at the moment are:
    - meta
    - Slots
    - Appointment
    - ServiceRequest
    - registry

    If there is no match in the pathsuffix returns null
*/
    if (pathsuffix.includes('/meta')) {
    return 'meta'
    }
    if (pathsuffix.includes('/Slots')) {
    return 'slots'
    }
    if (pathsuffix.includes('/Appointment')) {
    return 'appointment'
    }
    if (pathsuffix.includes('/ServiceRequest')) {
    return 'serviceRequest'
    }
    if (pathsuffix.includes('/registry')) {
    return 'registry'
    }
    return null
}
