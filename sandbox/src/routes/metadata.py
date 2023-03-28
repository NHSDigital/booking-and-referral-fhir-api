from fastapi import APIRouter, Header
from .example_loader import load_example
from fastapi.responses import JSONResponse

route = APIRouter()


@route.get("/metadata")
def get_metadata(
    NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier"),
    NHSD_End_User_Organisation: str = Header(..., alias="NHSD-End-User-Organisation"),
    NHSD_Requesting_Software: str = Header(..., alias="NHSD-Requesting-Software"),
    Accept: str = Header(None)
):
    return load_example("metadata/GET-success.json")


@route.post("/metadata")
@route.put("/metadata")
@route.patch("/metadata")
@route.delete("/metadata")
def metadata_method_not_allowed():
    headers = {"Allow": "GET"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)
