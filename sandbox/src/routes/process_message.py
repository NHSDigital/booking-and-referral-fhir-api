from fastapi import APIRouter, Header
from .example_loader import load_example
from fastapi.responses import JSONResponse

route = APIRouter()


@route.post("/$process-message")
def post_process_message(
    NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier"),
    NHSD_End_User_Organisation: str = Header(..., alias="NHSD-End-User-Organisation"),
    NHSD_Requesting_Software: str = Header(..., alias="NHSD-Requesting-Software"),
    Accept: str = Header(None)
):
    return load_example("process_message/POST-success.json")


@route.get("/$process-message")
@route.put("/$process-message")
@route.patch("/$process-message")
@route.delete("/$process-message")
def process_message_method_not_allowed():
    headers = {"Allow": "POST"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)
