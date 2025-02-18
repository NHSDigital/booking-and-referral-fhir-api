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
    EXCLUDED_HEADERS = {"host", "connection", "expect", "x-forwarded-for", "x-forwarded-proto", "x-forwarded-port"}  # Add more if needed
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

    # if "access-control-allow-origin" in response.headers:
    #     response.headers["access-control-allow-origin"] = "*"

    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))


@route.get("/DocumentReference")
async def get_document_reference(request: Request):
    query_string = urlencode(request.query_params)  # Preserve query params
    target = f"{NRLSandboxUrl}?{query_string}" if query_string else NRLSandboxUrl
    logger.info(f"GET request target: {target}")
    filteredHeaders = filter_headers(dict(request.headers))
    logger.error(f"request headers: {filteredHeaders}")
    logger.info("Sending Request")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(target, headers=filteredHeaders)
    except httpx.TimeoutException as e:
        logger.exception("Request timed out")
        return JSONResponse(content={"error": "Request timed out"}, status_code=504)
    except Exception as e:
        logger.exception("An error occurred")
        return JSONResponse(content={"error": "An error occurred"}, status_code=500)


    received_headers = dict(response.headers)

    logger.info(f"Got result back from target: {response.content}")

    # if "access-control-allow-origin" in received_headers:
    #     del received_headers["access-control-allow-origin"]

    # received_headers["access-control-allow-origin"] = "*"

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

    target = "https://sandbox.api.service.nhs.uk/record-locator/consumer/FHIR/R4/DocumentReference?subject%3Aidentifier=https%3A%2F%2Ffhir.nhs.uk%2FId%2Fnhs-number%7C9876543210&type=http%3A%2F%2Fsnomed.info%2Fsct%7C749001000000101&category=http%3A%2F%2Fsnomed.info%2Fsct%7C419891008"

    headers = {
        "accept": "application/fhir+json;version=1.1.0",
        "content-type": "application/fhir+json;version=1.1.0",
        "nhsd-end-user-organisation-ods": "V4T0L",
        "x-request-id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
        "x-correlation-id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
     }

    logger.info(f"PUT request target: {target} headers: {headers}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(target, headers=headers)
    except httpx.TimeoutException as e:
        logger.exception("Request timed out")
        return JSONResponse(content={"error": "Request timed out"}, status_code=504)
    except Exception as e:
        logger.exception("An error occurred")
        return JSONResponse(content={"error": "An error occurred"}, status_code=500)


    logger.info(f"GET response from NRL: {response.content}")
    for handler in logger.handlers:
        handler.flush()

    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

    # async with httpx.AsyncClient() as client:
    #     response = await client.put(target, headers=filter_headers(dict(request.headers)), data=await request.body())
    # logger.info(f"PUT request target: {target}")

    # return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))


@route.delete("/DocumentReference/{id}")
async def delete_document_reference_by_id(request: Request):
    query_string = urlencode(request.query_params)  # Preserve query params
    nrLSandboxUrl = NRLSandboxUrl+"/{id}"
    target = f"{nrLSandboxUrl}?{query_string}" if query_string else nrLSandboxUrl
    logger.info(f"DELETE request target: {target}")

    async with httpx.AsyncClient() as client:
        response = await client.delete(target, headers=filter_headers(dict(request.headers)))

    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
