from fastapi import APIRouter, Header, Response, status, Query
from uuid import UUID
from pydantic import BaseModel
from .example_loader import load_example
from .models import Profile
from fastapi.responses import JSONResponse

route = APIRouter()

existing_appointment_id = "c3f6145e-1a26-4345-b3f2-dccbcba62049"
ENTITY_NOT_FOUND = (
    status.HTTP_404_NOT_FOUND
)


class ServiceRequestBody(BaseModel):
    resourceType: str
    meta: Profile


@route.get("/ServiceRequest")
def get_service_request(
        patientIdentifier: str = Query(..., alias="patient:identifier"),
        NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier"),
):
    return load_example("service_request/GET-success.json")


@route.get("/ServiceRequest/{id}")
def get_service_request_id(
    response: Response,
    id: UUID,
    NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier"),
):
    if str(id) == existing_appointment_id:
        return load_example("service_request/id/GET-success.json")
    else:
        response.status_code = ENTITY_NOT_FOUND
        return load_example("OperationOutcome/REC/404-REC_NOT_FOUND-not-found.json")


@route.post("/ServiceRequest")
@route.put("/ServiceRequest")
@route.patch("/ServiceRequest")
@route.delete("/ServiceRequest")
def service_request_method_not_allowed():
    headers = {"Allow": "GET"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)


@route.patch("/ServiceRequest/{id}")
@route.put("/ServiceRequest/{id}")
@route.post("/ServiceRequest/{id}")
@route.delete("/ServiceRequest/{id}")
def service_request_id_method_not_allowed():
    headers = {"Allow": "GET"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)
