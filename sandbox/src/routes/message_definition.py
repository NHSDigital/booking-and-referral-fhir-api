from fastapi import APIRouter, Header
from .example_loader import load_example
from fastapi.responses import JSONResponse

route = APIRouter()


@route.get("/MessageDefinition")
def get_message_definition(
    context: str,
    NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier")
):
    return load_example("message_definition/MessageDefinition_ ServiceRequest-request_CaseTransfer.json")


@route.post("/MessageDefinition")
@route.put("/MessageDefinition")
@route.patch("/MessageDefinition")
@route.delete("/MessageDefinition")
def message_definition_method_not_allowed():
    headers = {"Allow": "GET"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)
