from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from .example_loader import load_example

route = APIRouter()


@route.get("/errors/{path}")
def errors(NHSD_Service: str = Header(...)):
    if str(NHSD_Service) == "NHS0001-401":
        response = load_example("unauthorized.json")
        status_code = 401
    if str(NHSD_Service) == "NHS0001-403":
        response = load_example("forbidden.json")
        status_code = 403
    if str(NHSD_Service) == "NHS0001-409":
        response = load_example("conflict.json")
        status_code = 409

    return JSONResponse(response, status_code=status_code)
