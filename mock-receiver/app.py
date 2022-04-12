import json
import os
import re
from dataclasses import dataclass
from typing import Callable
from urllib import parse

current_dir = os.path.dirname(os.path.realpath(__file__))


def load_example(path):
    with open(f'{current_dir}/examples/{path}') as f:
        return f.read().strip()


@dataclass
class EventMatch:
    # Request matching
    path: str
    method: str
    # Create Response
    # this lambda receives a dict {id, headers} and produces a response (see make_response). id as in /Appointment/{id}
    get_example: Callable[[dict], dict] = lambda _: ""

    def get_example_response(self, e):
        path = e["pathParameters"]["proxy"]
        is_matched = re.match(self.path, path) and self.method == e["httpMethod"]
        if is_matched:
            parts = parse.urlparse(path).path.split('/')
            path_id = parts[1] if len(parts) >= 2 else ""
            arg = {'path': path, 'id': path_id, 'headers': e['headers']}

            return self.get_example(arg)
        else:
            return None


def make_response(body_or_path: str, status_code: int = 200, headers=None):
    if body_or_path.endswith(".json") or body_or_path.endswith(".txt"):
        body = load_example(body_or_path)
    else:
        body = body_or_path

    if headers is None:
        headers = {"Content-Type": "application/json"}
    else:
        headers["Content-Type"] = "application/json"

    return {
        "statusCode": status_code,
        "headers": headers,
        "body": body
    }


def make_error_response(nhsd_service: str):
    def _make_response(_status_code: int, example_path: str):
        return {
            "statusCode": _status_code,
            "headers": {"Content-Type": "application/json"},
            "body": load_example(example_path)
        }

    if str(nhsd_service) == "NHS0001-401":
        return _make_response(401, "unauthorized.json")

    if str(nhsd_service) == "NHS0001-403":
        return _make_response(403, "forbidden.json")

    if str(nhsd_service) == "NHS0001-406":
        return _make_response(406, "not-acceptable.json")

    if str(nhsd_service) == "NHS0001-409":
        return _make_response(409, "conflict.json")

    if str(nhsd_service) == "NHS0001-422":
        return _make_response(422, "unprocessable-entity.json")

    if str(nhsd_service) == "NHS0001-500":
        return _make_response(500, "server-error.json")

    if str(nhsd_service) == "NHS0001-501":
        return _make_response(501, "not-implemented.json")

    if str(nhsd_service) == "NHS0001-503":
        return _make_response(503, "unavailable.json")


existing_appointment_id = load_example("appointment/POST-success.txt")
uuid4hex = r'[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}$'
event_to_response = [
    # Appointment
    EventMatch(path="^Appointment$", method="GET",
               get_example=lambda _: make_response("appointment/GET-success.json")),

    EventMatch(path="^Appointment$", method="POST",
               get_example=lambda _: make_response("appointment/POST-success.txt", 201)),

    EventMatch(path=f"^Appointment/{uuid4hex}$", method="GET",
               get_example=lambda r: make_response("appointment/id/GET-success.json")
               if r['id'] == existing_appointment_id else make_response("entity-not-found.json", 403)),

    # Fixme: Add a catch route for GET /Appointment/not-uuid

    EventMatch(path=rf"^Appointment/{uuid4hex}$", method="PATCH",
               get_example=lambda r: make_response("")
               if r['id'] == existing_appointment_id else make_response("entity-not-found.json", 403)),

    EventMatch(path=rf"^Appointment/{uuid4hex}$", method="PUT",
               get_example=lambda r: make_response("")
               if r['id'] == existing_appointment_id else make_response("entity-not-found.json", 403)),

    EventMatch(path=r"^Appointment/.*", method="POST",
               get_example=lambda _: make_response("method-not-allowed.json", 405,
                                                   {"Allow": "GET, PATCH, PUT, DELETE"})),
    EventMatch(path=r"^Appointment$", method="PUT",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET, POST"})),
    EventMatch(path=r"^Appointment$", method="PATCH",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET, POST"})),
    EventMatch(path=r"^Appointment$", method="DELETE",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET, POST"})),

    # metadata
    EventMatch(path=r"^metadata$", method="GET",
               get_example=lambda _: make_response("metadata/GET-success.json")),

    EventMatch(path=r"^metadata$", method="POST",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET"})),
    EventMatch(path=r"^metadata$", method="PUT",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET"})),
    EventMatch(path=r"^metadata$", method="PATCH",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET"})),
    EventMatch(path=r"^metadata$", method="DELETE",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET"})),

    # $process-message
    EventMatch(path=r"^\$process-message$", method="POST",
               get_example=lambda _: make_response("process_message/POST-success.json")),

    EventMatch(path=r"^\$process-message$", method="GET",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "POST"})),
    EventMatch(path=r"^\$process-message$", method="PUT",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "POST"})),
    EventMatch(path=r"^\$process-message$", method="PATCH",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "POST"})),
    EventMatch(path=r"^\$process-message$", method="DELETE",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "POST"})),

    # ServiceRequest
    EventMatch(path=r"^ServiceRequest$", method="GET",
               get_example=lambda _: make_response("service_request/GET-success.json")),
    EventMatch(path=rf"^ServiceRequest/{uuid4hex}$", method="GET",
               get_example=lambda r: make_response("service_request/id/GET-success.json")),
    EventMatch(path=r"^ServiceRequest$", method="POST",
               get_example=lambda _: make_response("", 201)),
    EventMatch(path=rf"^ServiceRequest/{uuid4hex}$", method="PUT",
               get_example=lambda r: make_response("service_request/id/PUT-success.json")),
    EventMatch(path=rf"^ServiceRequest/{uuid4hex}$", method="PATH",
               get_example=lambda r: make_response("service_request/id/PATCH-success.json")),
    EventMatch(path=r"^ServiceRequest$", method="DELETE",
               get_example=lambda _: make_response("")),

    EventMatch(path=r"^ServiceRequest$", method="PUT",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET, POST"})),
    EventMatch(path=r"^ServiceRequest$", method="PATCH",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET, POST"})),
    EventMatch(path=r"^ServiceRequest$", method="DELETE",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET, POST"})),
    EventMatch(path=rf"^ServiceRequest/{uuid4hex}$", method="DELETE",
               get_example=lambda _: make_response("method-not-allowed.json", 405,
                                                   {"Allow": "GET, PATCH, PUT, DELETE"})),

    # MessageDefinition
    EventMatch(path=r"^MessageDefinition$", method="GET",
               get_example=lambda _:
               make_response("message_definition/MessageDefinition_ ServiceRequest-request_CaseTransfer.json")),

    EventMatch(path=r"^MessageDefinition$", method="POST",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET"})),
    EventMatch(path=r"^MessageDefinition$", method="PUT",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET"})),
    EventMatch(path=r"^MessageDefinition$", method="PATCH",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET"})),
    EventMatch(path=r"^MessageDefinition$", method="DELETE",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET"})),

    # slots
    EventMatch(path=r"^slots/.*", method="GET",
               get_example=lambda r: make_error_response(r['headers']['NHSD_Service'])),

    # Header: errors
    EventMatch(path=r"^errors/.*", method="GET",
               get_example=lambda r: make_error_response(r['headers']['NHSD_Service'])),
]


def process_event(request_event):
    # TODO: Validate headers here
    for _event in event_to_response:
        response = _event.get_example_response(request_event)
        if response:
            return response

    return {
        "statusCode": 404,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": "route not found"})
    }


def handler(_event, context):
    return process_event(_event)


# Use this to fake a request for quick testing
if __name__ == '__main__':
    event = {
        "pathParameters": {
            "proxy": "Appointment/c3f6145e-1a26-4345-b3f2-dccbcba62049"
        },
        "httpMethod": "GET",
        "headers": {}
    }
    handler(event, None)
