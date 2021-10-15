from fastapi import APIRouter, Header
from .example_loader import load_example


route = APIRouter()


@route.post("/$process-message")
def post_process_message(NHSD_Service: str = Header(...), NHSD_Token: str = Header(...)):
    return load_example("process_message/POST-success.json")
