var b64 = JSON.parse(context.getVariable("b64decoded"));
context.setVariable("epc.path", "/endpoint-catalogue/FHIR/R4/Endpoint");
// Raw (unencoded) value — AM.PrepareEpcRequest passes it via <QueryParams> so Apigee handles encoding
context.setVariable("epc.identifier", b64.system + "|" + b64.value);

// EPC host: read from the booking-and-referral-epc-config KVM (key: epc_base_url, loaded by
// KVM.GetEpcConfig into private.epcBaseUrl). SC.CallEpc prepends https:// at the policy level
// (a fully-variable URL fails Apigee import with ProtocolMissingInURL), so strip any scheme the
// KVM value may carry to avoid https://https://...
var epcBaseUrl = context.getVariable("private.epcBaseUrl");
context.setVariable("private.epcHost", epcBaseUrl ? epcBaseUrl.replace(/^https?:\/\//, "") : "");

// EPC organisation ODS is the *requesting* organisation's own ODS, taken per-request from the
// caller's NHSD-End-User-Organisation header (base64 FHIR Organization, decoded into
// endUserOrgDecoded by Python.DecodeEndUserOrg). The EPC scopes Endpoint visibility to this ODS
// and cross-checks it against the token, so it must not be a fixed value.
// Open question INV013 Q4: the exact auth/ODS mechanism on the proxy's internal EPC hop.
var epcOrganisation = "";
var orgRaw = context.getVariable("endUserOrgDecoded");
if (orgRaw) {
    try {
        var org = JSON.parse(orgRaw);
        var idents = org.identifier || [];
        for (var i = 0; i < idents.length; i++) {
            if (idents[i].system === "https://fhir.nhs.uk/Id/ods-organization-code" && idents[i].value) {
                epcOrganisation = idents[i].value;
                break;
            }
        }
    } catch (e) {}
}
context.setVariable("private.epcOrganisation", epcOrganisation);
