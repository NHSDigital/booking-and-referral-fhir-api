from uuid import UUID

from fastapi import APIRouter, Header, Response, status, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .example_loader import load_example
from .models import Profile


class AppointmentBody(BaseModel):
    resourceType: str
    meta: Profile


route = APIRouter()

existing_appointment_id = "c3f6145e-1a26-4345-b3f2-dccbcba62049"
existing_appointment2_id = "91607239-b002-470a-8709-6b25bd50fdd1"
ENTITY_NOT_FOUND = (
    status.HTTP_404_NOT_FOUND
)


@route.get("/Appointment")
def get_appointment(
    patientIdentifier: str = Query(..., alias="patient:identifier"),
    NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier"),
):
    return load_example("appointment/GET-success.json")


@route.post("/Appointment")
def post_appointment(appointment: AppointmentBody):
    return load_example("appointment/POST-success.json")


@route.put("/Appointment")
@route.patch("/Appointment")
@route.delete("/Appointment")
def appointment_method_not_allowed():
    headers = {"Allow": "GET, POST"}
    return JSONResponse(
        load_example("method-not-allowed.json"), status_code=405, headers=headers
    )


@route.get("/Appointment/{id}")
def get_appointment_id(
    response: Response,
    id: UUID,
    NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier"),
):
    if str(id) == existing_appointment_id or str(id) == existing_appointment2_id:
        return load_example("appointment/id/GET-success.json")
    else:
        response.status_code = ENTITY_NOT_FOUND
        return load_example("OperationOutcome/REC/404-REC_NOT_FOUND-not-found.json")


@route.patch("/Appointment/{id}")
def patch_appointment(appointment: AppointmentBody):
    return load_example("appointment/POST-success.json")


@route.put("/Appointment/{id}")
def put_appointment(appointment: AppointmentBody):
    return load_example("appointment/POST-success.json")


@route.delete("/Appointment/{id}")
def delete_appointment(id: UUID):
    if str(id) == existing_appointment_id or str(id) == existing_appointment2_id:
        load_example("200_PUT.json")
        return
    else:
        return JSONResponse(
            load_example("entity-not-found.json"), status_code=404
        )


@route.post("/Appointment/{id}")
def appointment_id_method_not_allowed():
    headers = {"Allow": "GET, PATCH, PUT, DELETE"}
    return JSONResponse(
        load_example("method-not-allowed.json"), status_code=405, headers=headers
    )
