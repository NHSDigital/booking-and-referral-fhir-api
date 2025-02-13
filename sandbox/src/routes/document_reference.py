from urllib.parse import urlencode
from fastapi import APIRouter, Request, Response
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

route = APIRouter()

NRLSandboxUrl = "https://sandbox.api.service.nhs.uk/record-locator/consumer/FHIR/R4/DocumentReference"


def filter_headers(headers):
    EXCLUDED_HEADERS = {"host", "connection", "expect", "authorization"}  # Add more if needed
    headers = {k: v for k, v in headers.items() if k.lower() not in EXCLUDED_HEADERS}
    logger.info(f"Filtered request headers: {headers}")
    return headers


@route.get("/DocumentReference/{id}")
async def get_document_reference_by_id(request: Request):
    query_string = urlencode(request.query_params)  # Preserve query params
    nrLSandboxUrl = NRLSandboxUrl+"/{id}"
    target = f"{nrLSandboxUrl}?{query_string}" if query_string else nrLSandboxUrl
    logger.info(f"GET request target: {target}")

    async with httpx.AsyncClient() as client:
        response = await client.get(target, headers=filter_headers(dict(request.headers)))

    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))


@route.get("/DocumentReference")
async def get_document_reference(request: Request):
    query_string = urlencode(request.query_params)  # Preserve query params
    target = f"{NRLSandboxUrl}?{query_string}" if query_string else NRLSandboxUrl
    logger.info(f"GET request target: {target}")

    async with httpx.AsyncClient() as client:
        response = await client.get(target, headers=filter_headers(dict(request.headers)))

    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))


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
