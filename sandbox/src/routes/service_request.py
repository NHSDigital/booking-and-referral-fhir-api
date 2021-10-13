from fastapi import APIRouter, Header
from uuid import UUID
from .examples.example_loader import load_example
from pydantic import BaseModel


route = APIRouter()


class Profile(BaseModel):
    profile: list


class ServiceRequestBody(BaseModel):
    resourceType: str
    meta: Profile


@route.get("/ServiceRequest")
def get_service_request(
    patientIdentifier: str, NHSD_Service: str = Header(...)
):
    return load_example("service_request/GET-success.json")


@route.post("/ServiceRequest", status_code=201)
def post_service_request(
    body: ServiceRequestBody, NHSD_Service: str = Header(...)
):
    return ""


@route.get("/ServiceRequest/{id}")
def get_service_request_id(id: UUID, NHSD_Service: str = Header(...)):
    return load_example("service_request/id/GET-success.json")


@route.patch("/ServiceRequest/{id}")
def patch_service_request_id(id: UUID, NHSD_Service: str = Header(...)):
    return load_example("service_request/id/PATCH-success.json")


@route.put("/ServiceRequest/{id}")
def put_service_request_id(id: UUID, NHSD_Service: str = Header(...)):
    return load_example("service_request/id/PUT-success.json")


@route.delete("/ServiceRequest/{id}")
def delete_service_request_id(id: UUID, NHSD_Service: str = Header(...)):
    return ""
