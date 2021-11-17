from fastapi import APIRouter, Header
from .example_loader import load_example
from fastapi.responses import JSONResponse

route = APIRouter()


@route.post("/$process-message")
def post_process_message(NHSD_Service: str = Header(...), NHSD_Token: str = Header(...)):
    return load_example("process_message/POST-success.json")


@route.get("/$processmessage")
@route.put("/$processmessage")
@route.patch("/$processmessage")
@route.delete("/$processmessage")
def process_message_method_not_allowed():
    headers = {"Allow": "POST"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)
