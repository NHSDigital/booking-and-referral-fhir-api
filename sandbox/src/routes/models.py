from pydantic import BaseModel
from typing import List


class Profile(BaseModel):
    profile: List[str]


class ServiceRequestBody(BaseModel):
    resourceType: str
    meta: Profile


class AppointmentBody(BaseModel):
    resourceType: str
    meta: Profile


class DocumentReferenceRequestBody(BaseModel):
    resourceType: str
    meta: Profile
