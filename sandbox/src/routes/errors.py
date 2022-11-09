import base64
import json

from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from .example_loader import load_example

route = APIRouter()


@route.get("/errors/{path}")
def errors(NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier")):
    decoded = base64.b64decode(NHSD_Target_Identifier)
    target_id = json.loads(decoded)["value"]

    response = {"message": "no match for target id"}
    status_code = 400
    if target_id == "NHS0001-401":
        response = load_example("unauthorized.json")
        status_code = 401
    if target_id == "NHS0001-403":
        response = load_example("forbidden.json")
        status_code = 403
    if target_id == "NHS0001-406":
        response = load_example("not-acceptable.json")
        status_code = 406
    if target_id == "NHS0001-408":
        response = {}
        status_code = 408
    if target_id == "NHS0001-409":
        response = load_example("conflict.json")
        status_code = 409
    if target_id == "NHS0001-422":
        response = load_example("unprocessable-entity.json")
        status_code = 422
    if target_id == "NHS0001-500":
        response = load_example("server-error.json")
        status_code = 500
    if target_id == "NHS0001-500-1":
        response = {}
        status_code = 500
    if target_id == "NHS0001-500-2":
        response = load_example("OperationOutcome/REC/500-REC_SERVER_ERROR-no-store.json")
        status_code = 500
    if target_id == "NHS0001-501":
        response = load_example("not-implemented.json")
        status_code = 501
    if target_id == "NHS0001-503":
        response = {}
        status_code = 503

    return JSONResponse(response, status_code=status_code)
