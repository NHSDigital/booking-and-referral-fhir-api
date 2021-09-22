from fastapi import APIRouter, Header
from .examples.example_loader import load_example


route = APIRouter()


@route.post("/$process-message")
def post_process_message(NHSD_ServiceIdentifier: str = Header(...)):
    return load_example("process_message/POST-success.json")
