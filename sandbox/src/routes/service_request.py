from fastapi import APIRouter, Header
from uuid import UUID
from pydantic import BaseModel
from .example_loader import load_example
from .models import Profile
from fastapi.responses import JSONResponse

route = APIRouter()


class ServiceRequestBody(BaseModel):
    resourceType: str
    meta: Profile


@route.get("/ServiceRequest")
def get_service_request(
        patientIdentifier: str, NHSD_Token: str = Header(...), NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier")
):
    return load_example("service_request/GET-success.json")


@route.get("/ServiceRequest/{id}")
def get_service_request_id(id: UUID, NHSD_Token: str = Header(...), NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier")):
    return load_example("service_request/id/GET-success.json")


@route.post("/ServiceRequest")
@route.put("/ServiceRequest")
@route.patch("/ServiceRequest")
@route.delete("/ServiceRequest")
def service_request_method_not_allowed():
    headers = {"Allow": "GET, POST"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)


@route.patch("/ServiceRequest/{id}")
@route.put("/ServiceRequest/{id}")
@route.post("/ServiceRequest/{id}")
@route.delete("/ServiceRequest/{id}")
def service_request_id_method_not_allowed():
    headers = {"Allow": "GET, PATCH, PUT, DELETE"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)
