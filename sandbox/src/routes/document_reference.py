from fastapi import APIRouter
from uuid import UUID
from .example_loader import load_example
from pydantic import BaseModel


class Profile(BaseModel):
    profile: list


class DocumentReferenceRequestBody(BaseModel):
    resourceType: str
    meta: Profile


route = APIRouter()


@route.post("/DocumentReference", status_code=201)
def post_document_reference(body: DocumentReferenceRequestBody):
    return load_example("document_reference/POST-success.json")


@route.get("/DocumentReference")
def get_document_reference(patientIdentifier: str):
    return load_example("document_reference/GET-success.json")


@route.get("/DocumentReference/{id}")
def get_document_reference_id(id: UUID):
    return load_example("document_reference/id/GET-success.json")


@route.put("/DocumentReference/{id}")
def put_document_reference_id(body: DocumentReferenceRequestBody, id: UUID):
    return ""


@route.delete("/DocumentReference/{id}")
def delete_document_reference_id(id: UUID):
    return ""
