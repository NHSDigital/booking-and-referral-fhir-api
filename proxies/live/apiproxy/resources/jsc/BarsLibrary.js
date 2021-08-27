/*
    This file should hold functions specific to this proxy.
    This way we can share functions between javascript policies.
    In order to load this library in your javascript policy
    use the tag <IncludeURL>jsc://BarsLibrary.js</IncludeURL>
    for reference see:
    https://www.googlecloudcommunity.com/gc/Apigee/Can-you-include-a-Javascript-in-another-Javascript/m-p/59862#M51664

*/

function set_variables(location, vars) {
    /*
      Unpacks the values from a kvm and publish them as context variables.
      The kvm should be a JSON structure.
      location: str
      vars: JSON object

    */
    if (typeof vars !== 'object') {
        return;
    }

    for (var key in vars)
    {
        if (!vars.hasOwnProperty(key))
            continue;
        variable = location + '.' + key;
        value = vars[key];
        if (typeof value === 'object' && value !== null) {
            set_variables(variable, value);
        }
        else {
            context.setVariable(variable, value);
        }
    }
}


function get_target_url_from_kvm(serviceId, endpoint) {
    /*
      Get a url value from the booking-and-referral kvm.
      the valid endpoints at the moment are:
      - meta
      - slots
      
      If there is no value in the kvm it returns null
    */
      var location = "booking-and-referral-config.NHSD-ServiceIdentifier." + serviceId + "." + endpoint;
      var url = context.getVariable(location);
      return url
  }


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
