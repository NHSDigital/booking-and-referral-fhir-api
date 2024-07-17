import base64

b64encoded = flow.getVariable("request.header.NHSD-Target-Identifier")
b64decoded = base64.b64decode(b64encoded)

b64encodedTarget = flow.getVariable("booking-and-referral-config")
#b64decodedTarget = base64.b64decode(b64encodedTarget)

flow.setVariable("b64decoded", b64decoded)
#flow.setVariable("b64decodedTarget", b64decodedTarget)
flow.setVariable("b64decodedTarget", b64encodedTarget)
