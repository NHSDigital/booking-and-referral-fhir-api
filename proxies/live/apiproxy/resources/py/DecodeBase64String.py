import base64

b64encoded = flow.getVariable("request.header.NHSD-Target-Identifier")
b64decoded = base64.b64decode(b64encoded)

flow.setVariable("b64decoded", b64decoded)
