from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from enum import Enum
from datetime import datetime
from .example_loader import load_example

route = APIRouter()


class Status(Enum):
    status_free = "free"
    status_busy = "busy"


class Include(Enum):
    schedule = "Schedule"
    practitioner = "Schedule:actor:Practitioner"
    practitioner_role = "Schedule:actor:PractitionerRole"
    health_care_service_include = "Schedule:actor:HealthcareService"
    provided_by = "HealthcareService.providedBy"
    location = "HealthcareService.location"


@route.get("/Slot")
def slot(
    healthcareService: str,
    status: Status,
    start: datetime,
    _include: Include,
    NHSD_Target_Identifier: str = Header(..., alias="NHSD-Target-Identifier"),
    X_Request_Id: str = Header(..., alias="X-Request-Id"),
    X_Correlation_Id: str = Header(..., alias="X-Correlation-Id"),
):
    return load_example("slots/GET-success.json")


@route.post("/Slot")
@route.put("/Slot")
@route.patch("/Slot")
@route.delete("/Slot")
def slot_method_not_allowed():
    headers = {"Allow": "GET"}
    return JSONResponse(
        load_example("method-not-allowed.json"), status_code=405, headers=headers
    )
