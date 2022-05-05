import json
import os
import re
from dataclasses import dataclass
from typing import Callable
from urllib import parse

from dateutil.parser import parse as date_parser

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
    # this lambda receives a dict {queries, id, headers} and produces
    # a response (see make_response). id as in /Appointment/{id}
    get_example: Callable[[dict], dict] = lambda _: ""

    def get_example_response(self, e):
        full_path = e["pathParameters"]["proxy"]
        if e.get("queryStringParameters"):
            query_params = e.get("queryStringParameters")
            query_params_name = list(query_params.keys())[0]
            query_params_value = query_params.get("patientIdentifier")
            full_path = e["pathParameters"]["proxy"] + "?" + query_params_name + "=" + query_params_value

        print("full_path")
        print(full_path)
        print("path")
        print(self.path)
        print("method")
        print(self.method)
        print(e["httpMethod"])
        print("match")
        print(re.match(self.path, full_path))
        print(self.method == e["httpMethod"])
        print(self.path == full_path and self.method == e["httpMethod"])

        is_matched = re.match(self.path, full_path) and self.method == e["httpMethod"]
        # is_matched = self.path == full_path and self.method == e["httpMethod"]
        if is_matched:
            print("match")
            parts = parse.urlparse(full_path).path.split('/')
            path_id = parts[1] if len(parts) >= 2 else ""
            arg = {'queries': e['multiValueQueryStringParameters'], 'id': path_id, 'headers': e['headers']}

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
    if str(nhsd_service) == "NHS0001-401":
        return make_response("unauthorized.json", 401)

    if str(nhsd_service) == "NHS0001-403":
        return make_response("forbidden.json", 403)

    if str(nhsd_service) == "NHS0001-406":
        return make_response("not-acceptable.json", 406)

    if str(nhsd_service) == "NHS0001-409":
        return make_response("conflict.json", 409)

    if str(nhsd_service) == "NHS0001-422":
        return make_response("unprocessable-entity.json", 422)

    if str(nhsd_service) == "NHS0001-500":
        return make_response("server-error.json", 500)

    if str(nhsd_service) == "NHS0001-501":
        return make_response("not-implemented.json", 501)

    if str(nhsd_service) == "NHS0001-503":
        return make_response("unavailable.json", 503)


def make_slots_response(queries: dict):
    def is_date(q):
        try:
            date_parser(q, fuzzy=False)
            return True
        except ValueError:
            return False

    if ("healthcareService" in queries and
            "status" in queries and set(queries['status']) <= {'free', 'busy'} and
            "start" in queries and is_date(queries['start'][0]) and
            "Schedule.actor:HealthcareService" in queries and
            "_include" in queries and set(queries["_include"]) <= {"Schedule", "Schedule:actor:Practitioner",
                                                                   "Schedule:actor:PractitionerRole",
                                                                   "Schedule:actor:HealthcareService",
                                                                   "HealthcareService.providedBy",
                                                                   "HealthcareService.location"}):

        return make_response("slots/GET-success.json", 200)

    else:
        return make_response("bad-request.json", 400)


existing_appointment_id = load_example("appointment/POST-success.txt")
uuid4hex = r'[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}$'
nhs_number_regex = r'[0-9]{10}$'

event_to_response = [
    # Appointment
    EventMatch(path=f"^Appointment?patientIdentifier={nhs_number_regex}$", method="GET",
               get_example=lambda _: make_response("appointment/GET-success.json")),

    EventMatch(path=r"^Appointment$", method="GET",
               get_example=lambda _: make_response("bad-request.json", 400)),

    EventMatch(path="^Appointment$", method="POST",
               get_example=lambda _: make_response("appointment/POST-success.txt", 201)),

    EventMatch(path=f"^Appointment/{uuid4hex}$", method="GET",
               get_example=lambda r: make_response("appointment/id/GET-success.json")
               if r['id'] == existing_appointment_id else make_response("entity-not-found.json", 403)),

    EventMatch(path=rf"^Appointment/{uuid4hex}$", method="PATCH",
               get_example=lambda r: make_response("/""/")
               if r['id'] == existing_appointment_id else make_response("entity-not-found.json", 403)),

    EventMatch(path=rf"^Appointment?patientIdentifier={nhs_number_regex}$", method="PUT",
               get_example=lambda r: make_response("")
               if r['id'] == existing_appointment_id else make_response("entity-not-found.json", 403)),

    EventMatch(path=r"^Appointment/.*", method="POST",
               get_example=lambda _: make_response("method-not-allowed.json", 405,
                                                   {"Allow": "GET, PATCH, PUT, DELETE"})),
    EventMatch(path=r"^Appointment$", method="PUT",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET, POST"})),

    EventMatch(path=r"^Appointment$", method="PATCH",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET, POST"})),

    EventMatch(path=r"Appointment", method="DELETE",
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
    EventMatch(path=r"^Slot?.*", method="GET",
               get_example=lambda r: make_slots_response(r['queries'])),

    EventMatch(path=r"^Slot$", method="POST",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET"})),
    EventMatch(path=r"^Slot$", method="PUT",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET"})),
    EventMatch(path=r"^Slot$", method="PATCH",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET"})),
    EventMatch(path=r"^Slot$", method="DELETE",
               get_example=lambda _: make_response("method-not-allowed.json", 405, {"Allow": "GET"})),

    # Header: errors
    EventMatch(path=r"^errors/.*", method="GET",
               get_example=lambda r: make_error_response(r['headers']['NHSD_Service'])),
]


def process_event(request_event):
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
    print(_event)
    return process_event(_event)


# Use this to fake a request for quick local testing
if __name__ == '__main__':
    event = {
        "pathParameters": {
            "proxy": "Slots?healthcareService=foo&status=free&"
                     "_include=Schedule&Schedule.actor:HealthcareService=foo&start=20220301"
        },
        "httpMethod": "GET",
        "headers": {}
    }

    print(handler(event, None))
