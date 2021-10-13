from fastapi import APIRouter, Header
from .examples.example_loader import load_example


route = APIRouter()


@route.get("/metadata")
def get_appointment(NHSD_Service: str = Header(...)):
    return load_example("metadata/GET-success.json")
