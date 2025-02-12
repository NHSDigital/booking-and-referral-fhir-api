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


@route.post("/ServiceRequest")
def post_appointment(servicerequest: ServiceRequestBody):
    return load_example("service_request/POST-success.json")


@route.put("/ServiceRequest")
@route.patch("/ServiceRequest")
@route.delete("/ServiceRequest")
def service_request_method_not_allowed():
    headers = {"Allow": "GET"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)


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


@route.patch("/ServiceRequest/{id}")
def patch_appointment(servicerequest: ServiceRequestBody):
    return load_example("service_request/POST-success.json")


@route.put("/ServiceRequest/{id}")
def put_appointment(servicerequest: ServiceRequestBody):
    return load_example("service_request/POST-success.json")


@route.delete("/ServiceRequest/{id}")
def delete_appointment(response: Response, id: UUID):
    if str(id) == existing_appointment_id :
        return load_example("200_PUT.json")
    else:
        response.status_code = ENTITY_NOT_FOUND
        load_example("entity-not-found.json")


@route.post("/ServiceRequest/{id}")
def appointment_id_method_not_allowed():
    headers = {"Allow": "GET, PATCH, PUT, DELETE"}
    return JSONResponse(
        load_example("method-not-allowed.json"), status_code=405, headers=headers
    )


