var b64 = JSON.parse(context.getVariable("b64decoded"));
var identifier = encodeURIComponent(b64.system + "|" + b64.value);
context.setVariable("epc.path", "/booking-and-referral/FHIR/R4/Endpoint?HealthcareService.identifier=" + identifier);
