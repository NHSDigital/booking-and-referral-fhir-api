from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from .example_loader import load_example

route = APIRouter()


@route.get("/MessageDefinition")
def get_message_definition(
        context: str,
        NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier"),
        NHSD_End_User_Organisation: str = Header(..., alias="NHSD-End-User-Organisation"),
        NHSD_Requesting_Software: str = Header(..., alias="NHSD-Requesting-Software"),
        Accept: str = Header(None)
):
    return load_example("message_definition/MessageDefinition_ServiceRequest-request_CaseTransfer.json")


@route.post("/MessageDefinition")
@route.put("/MessageDefinition")
@route.patch("/MessageDefinition")
@route.delete("/MessageDefinition")
def message_definition_method_not_allowed():
    headers = {"Allow": "GET"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)
