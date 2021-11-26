from fastapi import APIRouter, Header, Response, status
from uuid import UUID
from pydantic import BaseModel
from .example_loader import load_example
from .models import Profile
from fastapi.responses import JSONResponse


class AppointmentBody(BaseModel):
    resourceType: str
    meta: Profile


route = APIRouter()

existing_appointment_id = load_example("appointment/POST-success.txt")
ENTITY_NOT_FOUND = status.HTTP_403_FORBIDDEN  # Spec is probably wrong and status should be 404


@route.get("/Appointment")
def get_appointment(patientIdentifier: str, NHSD_Service: str = Header(...), NHSD_Token: str = Header(...)):
    return load_example("appointment/GET-success.json")


@route.post("/Appointment", status_code=201)
def create_appointment(NHSD_Service: str = Header(...), NHSD_Token: str = Header(...)):
    return load_example("appointment/POST-success.txt")


@route.get("/Appointment/{id}")
def get_appointment_id(response: Response, id: UUID, NHSD_Service: str = Header(...), NHSD_Token: str = Header(...)):
    if str(id) == existing_appointment_id:
        return load_example("appointment/id/GET-success.json")
    else:
        response.status_code = ENTITY_NOT_FOUND
        return load_example("entity-not-found.json")


@route.patch("/Appointment/{id}")
def patch_appointment_id(response: Response, body: AppointmentBody, id: UUID, NHSD_Service: str = Header(...), NHSD_Token: str = Header(...)):
    if str(id) == existing_appointment_id:
        return ""
    else:
        response.status_code = ENTITY_NOT_FOUND
        return load_example("entity-not-found.json")


@route.put("/Appointment/{id}")
def put_appointment_id(response: Response,
                       body: AppointmentBody, id: UUID, NHSD_Service: str = Header(...), NHSD_Token: str = Header(...)
                       ):
    if str(id) == existing_appointment_id:
        return ""
    else:
        response.status_code = ENTITY_NOT_FOUND
        return load_example("entity-not-found.json")


@route.delete("/Appointment/{id}")
def delete_appointment_id(response: Response, id: UUID, NHSD_Service: str = Header(...), NHSD_Token: str = Header(...)):
    if str(id) == existing_appointment_id:
        return ""
    else:
        response.status_code = ENTITY_NOT_FOUND
        return load_example("entity-not-found.json")


@route.put("/Appointment")
@route.patch("/Appointment")
@route.delete("/Appointment")
def appointment_method_not_allowed():
    headers = {"Allow": "GET, POST"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)


@route.post("/Appointment/{id}")
def appointment_id_method_not_allowed():
    headers = {"Allow": "GET, PATCH, PUT, DELETE"}
    return JSONResponse(load_example("method-not-allowed.json"), status_code=405, headers=headers)
