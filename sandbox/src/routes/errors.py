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
    if str(NHSD_Service) == "NHS0001-406":
        response = load_example("not-acceptable.json")
        status_code = 406
    if str(NHSD_Service) == "NHS0001-409":
        response = load_example("conflict.json")
        status_code = 409
    if str(NHSD_Service) == "NHS0001-422":
        response = load_example("unprocessable-entity.json")
        status_code = 422
    if str(NHSD_Service) == "NHS0001-500":
        response = load_example("server-error.json")
        status_code = 500
    if str(NHSD_Service) == "NHS0001-501":
        response = load_example("not-implemented.json")
        status_code = 501
    if str(NHSD_Service) == "NHS0001-503":
        response = load_example("unavailable.json")
        status_code = 503

    return JSONResponse(response, status_code=status_code)
