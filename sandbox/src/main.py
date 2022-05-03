import os

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from routes import (
    errors,
    slots,
    appointment,
    metadata,
    service_request,
    process_message,
    document_reference,
    message_definition,
)
from routes.example_loader import load_example

app = FastAPI()


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):

    if "Appointment" in str(request.url.path):
        response = load_example("bad-request.json")
        status_code = 400
    if "registry" in str(request.url.path):
        response = load_example("bad-request.json")
        status_code = 400
    if "$process-message" in str(request.url.path):
        response = load_example("bad-request.json")
        status_code = 400
    if "meta" in str(request.url.path):
        response = load_example("bad-request.json")
        status_code = 400
    if "ServiceRequest" in str(request.url.path):
        response = load_example("bad-request.json")
        status_code = 400
    if "Slot" in str(request.url.path):
        response = load_example("bad-request.json")
        status_code = 400
    if "DocumentReference" in str(request.url.path):
        response = load_example("bad-request.json")
        status_code = 400
    if "MessageDefinition" in str(request.url.path):
        response = load_example("bad-request.json")
        status_code = 400

    return JSONResponse(response, status_code=status_code)


app.include_router(errors.route)
app.include_router(slots.route)
app.include_router(appointment.route)
app.include_router(metadata.route)
app.include_router(service_request.route)
app.include_router(process_message.route)
app.include_router(document_reference.route)
app.include_router(message_definition.route)


@app.get("/_status")
def status():
    return Response(status_code=HTTP_200_OK)


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    uvicorn.run(app, host="10.0.0.1", port=port)
