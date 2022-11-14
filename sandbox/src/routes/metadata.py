from fastapi import APIRouter, Header
from .example_loader import load_example
from fastapi.responses import JSONResponse

route = APIRouter()


@route.get("/metadata")
def get_metadata(
    NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier"),
):
    return load_example("metadata/GET-success.json")


@route.post("/metadata")
@route.put("/metadata")
@route.patch("/metadata")
@route.delete("/metadata")
def metadata_method_not_allowed():
    headers = {"Allow": "GET"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)
