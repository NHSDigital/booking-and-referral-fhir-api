from fastapi import APIRouter, Header
from uuid import UUID
from .examples.example_loader import load_example
from pydantic import BaseModel


route = APIRouter()


class Profile(BaseModel):
    profile: list


class AppointmentBody(BaseModel):
    resourceType: str
    meta: Profile


@route.get("/Appointment")
def get_appointment(patientIdentifier: str, NHSD_ServiceIdentifier: str = Header(...)):
    return load_example("appointment/GET-success.json")


@route.post("/Appointment", status_code=201)
def create_appointment(NHSD_ServiceIdentifier: str = Header(...)):
    return load_example("appointment/POST-success.txt")


@route.get("/Appointment/{id}")
def get_appointment_id(id: UUID, NHSD_ServiceIdentifier: str = Header(...)):
    return load_example("appointment/id/GET-success.json")


@route.patch("/Appointment/{id}")
def patch_appointment_id(
    body: AppointmentBody, id: UUID, NHSD_ServiceIdentifier: str = Header(...)
):
    return ""


@route.put("/Appointment/{id}")
def put_appointment_id(
    body: AppointmentBody, id: UUID, NHSD_ServiceIdentifier: str = Header(...)
):
    return ""


@route.delete("/Appointment/{id}")
def delete_appointment_id(id: UUID, NHSD_ServiceIdentifier: str = Header(...)):
    return ""
