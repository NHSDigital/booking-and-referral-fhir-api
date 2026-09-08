import base64

b64encoded = flow.getVariable("request.header.NHSD-Target-Identifier")
b64decoded = base64.b64decode(b64encoded)

# LEGACY: b64decodedTarget is read by BarsLibrary.js in the S3 routing path.
# TO BE REMOVED together with the LegacyS3Routing flow in bref-target.xml.
b64encodedTarget = flow.getVariable("booking-and-referral-config")
#b64decodedTarget = base64.b64decode(b64encodedTarget)

flow.setVariable("b64decoded", b64decoded)
#flow.setVariable("b64decodedTarget", b64decodedTarget)
flow.setVariable("b64decodedTarget", b64encodedTarget)
