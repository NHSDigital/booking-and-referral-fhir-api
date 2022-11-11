import base64
import binascii

b64encoded = flow.getVariable("request.header.NHSD-Target-Identifier")
try:
    b64decoded = base64.b64decode(b64encoded)
    flow.setVariable("b64decoded", b64decoded)
except binascii.Error:
    flow.setVariable("b64decodedFailed", True)

