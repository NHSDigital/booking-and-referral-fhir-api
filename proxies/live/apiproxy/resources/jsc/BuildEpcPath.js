var b64 = JSON.parse(context.getVariable("b64decoded"));
context.setVariable("epc.path", "/endpoint-catalogue/FHIR/R4/Endpoint");
// Raw (unencoded) value — AM.PrepareEpcRequest passes it via <QueryParams> so Apigee handles encoding
context.setVariable("epc.identifier", b64.system + "|" + b64.value);

// SC.CallEpc hardcodes the https:// scheme so Apigee can validate the bundle at
// import time (a fully-variable URL fails with ProtocolMissingInURL). Strip any
// scheme the KVM value may carry so we never end up with https://https://...
// TEMP (RAA-7897): hardcode internal-dev EPC while booking-and-referral-epc-config KVM is being provisioned
context.setVariable("private.epcHost", "2y2lu2de0m.execute-api.eu-west-2.amazonaws.com");
context.setVariable("private.epcOrganisation", "RR81");
