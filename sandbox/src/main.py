import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes import (
    slots,
    appointment,
    metadata,
    service_request,
    process_message,
    document_reference,
)
from routes.examples.example_loader import load_example

app = FastAPI()


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    response = load_example("bad-request.json")
    return JSONResponse(response, status_code=400)


app.include_router(slots.route)
app.include_router(appointment.route)
app.include_router(metadata.route)
app.include_router(service_request.route)
app.include_router(process_message.route)
app.include_router(document_reference.route)


@app.get("/_status")
def status():
    return load_example("_status.json")


@app.get("/")
def index():
    # This is the endpoint that proxy calls to get health status
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
