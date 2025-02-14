from urllib.parse import urlencode
from fastapi import APIRouter, Request, Response
import httpx
import logging
import json
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

route = APIRouter()

NRLSandboxUrl = "https://sandbox.api.service.nhs.uk/record-locator/consumer/FHIR/R4/DocumentReference"


def filter_headers(headers):
    EXCLUDED_HEADERS = {"host", "connection", "expect"}  # Add more if needed
    headers = {k: v for k, v in headers.items() if k.lower() not in EXCLUDED_HEADERS}
    logger.info(f"Filtered request headers: {headers}")
    return headers


@route.get("/test")
async def test_document_reference(request: Request):
    query_string = urlencode(request.query_params)  # Preserve query params
    target = f"{NRLSandboxUrl}?{query_string}" if query_string else NRLSandboxUrl
    logger.info(f"GET request target: {target}")

    sent_headers = filter_headers(dict(request.headers))

    async with httpx.AsyncClient() as client:
        response = await client.get(target, headers=sent_headers)

    received_headers = dict(response.headers)
    received_body = response.json()

    result = {
        "target": target,
        "sent_headers": sent_headers,
        "received_headers": received_headers,
        "received_body": received_body
    }

    # Convert result to JSON and calculate content length
    result_json = json.dumps(result)

    # Remove Content-Length from received headers to avoid duplication
    if "content-length" in received_headers:
        del received_headers["content-length"]
    if "access-control-allow-origin" in received_headers:
        del received_headers["access-control-allow-origin"]

    received_headers["access-control-allow-origin"] = "*"

    # Update the response headers with the received headers and content length
    response_headers = {**received_headers}

    return JSONResponse(content=result_json, status_code=response.status_code, headers=response_headers)


@route.get("/DocumentReference/{id}")
async def get_document_reference_by_id(request: Request):
    query_string = urlencode(request.query_params)  # Preserve query params
    nrLSandboxUrl = NRLSandboxUrl+"/{id}"
    target = f"{nrLSandboxUrl}?{query_string}" if query_string else nrLSandboxUrl
    logger.info(f"GET request target: {target}")

    async with httpx.AsyncClient() as client:
        response = await client.get(target, headers=filter_headers(dict(request.headers)))

    if "access-control-allow-origin" in request.headers:
        request.headers["access-control-allow-origin"] = "*"

    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))


@route.get("/DocumentReference")
async def get_document_reference(request: Request):
    query_string = urlencode(request.query_params)  # Preserve query params
    target = f"{NRLSandboxUrl}?{query_string}" if query_string else NRLSandboxUrl
    logger.info(f"GET request target: {target}")

    async with httpx.AsyncClient() as client:
        response = await client.get(target, headers=filter_headers(dict(request.headers)))

    received_headers = dict(response.headers)

    if "access-control-allow-origin" in received_headers:
        received_headers["access-control-allow-origin"] = "*"

    return Response(content=response.content, status_code=response.status_code, headers=received_headers)


@route.post("/DocumentReference")
async def post_document_reference(request: Request):
    query_string = urlencode(request.query_params)  # Preserve query params
    target = f"{NRLSandboxUrl}?{query_string}" if query_string else NRLSandboxUrl
    logger.info(f"POST request target: {target}")

    async with httpx.AsyncClient() as client:
        response = await client.post(target, headers=filter_headers(dict(request.headers)), data=await request.body())

    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))


@route.put("/DocumentReference/{id}")
async def put_document_reference_by_id(request: Request):
    query_string = urlencode(request.query_params)  # Preserve query params
    nrLSandboxUrl = NRLSandboxUrl+"/{id}"
    target = f"{nrLSandboxUrl}?{query_string}" if query_string else nrLSandboxUrl

    async with httpx.AsyncClient() as client:
        response = await client.put(target, headers=filter_headers(dict(request.headers)), data=await request.body())
    logger.info(f"PUT request target: {target}")

    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))


@route.delete("/DocumentReference/{id}")
async def delete_document_reference_by_id(request: Request):
    query_string = urlencode(request.query_params)  # Preserve query params
    nrLSandboxUrl = NRLSandboxUrl+"/{id}"
    target = f"{nrLSandboxUrl}?{query_string}" if query_string else nrLSandboxUrl
    logger.info(f"DELETE request target: {target}")

    async with httpx.AsyncClient() as client:
        response = await client.delete(target, headers=filter_headers(dict(request.headers)))

    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
