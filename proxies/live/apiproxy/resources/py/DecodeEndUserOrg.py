import base64

b64encoded = flow.getVariable("request.header.NHSD-End-User-Organisation")
org_decoded = ""
if b64encoded:
    org_decoded = base64.b64decode(b64encoded)

flow.setVariable("endUserOrgDecoded", org_decoded)
