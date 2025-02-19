from fastapi import APIRouter
import logging
from tests.example_loader import load_example

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

route = APIRouter()


@route.get("/DocumentReference/{id}")
async def get_document_reference_by_id():
    return load_example("document_reference/id/GET-success.json")


@route.get("/DocumentReference")
async def get_document_reference():
    return load_example("document_reference/GET-success.json")


@route.post("/DocumentReference")
async def post_document_reference():
    return load_example("document_reference/POST-success.json")


@route.put("/DocumentReference/{id}")
async def put_document_reference_by_id():
    return load_example("document_reference/POST-success.json")


@route.delete("/DocumentReference/{id}")
async def delete_document_reference_by_id():
    return load_example("document_reference/DELETE-success.json")
