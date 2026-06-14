var b64 = JSON.parse(context.getVariable("b64decoded"));
var identifier = encodeURIComponent(b64.system + "|" + b64.value);
context.setVariable("epc.path", "/booking-and-referral/FHIR/R4/Endpoint?HealthcareService.identifier=" + identifier);

// SC.CallEpc hardcodes the https:// scheme so Apigee can validate the bundle at
// import time (a fully-variable URL fails with ProtocolMissingInURL). Strip any
// scheme the KVM value may carry so we never end up with https://https://...
var epcBaseUrl = context.getVariable("private.epcBaseUrl") || "";
context.setVariable("private.epcHost", epcBaseUrl.replace(/^https?:\/\//, ""));
