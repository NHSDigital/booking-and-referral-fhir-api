import json
import os
import re
from dataclasses import dataclass, field


@dataclass
class EventMatch:
    # Request matching
    path: str
    method: str
    # Response fields
    example_path: str
    status_code: int = 200
    headers: dict = field(default_factory=lambda: {"Content-Type": "application/json"})

    __current_dir = os.path.dirname(os.path.realpath(__file__))

    def match(self, e) -> bool:
        return re.match(self.path, e["pathParameters"]["proxy"]) and self.method == e["httpMethod"]

    def make_response(self):
        return {
            "statusCode": self.status_code,
            "headers": self.headers,
            "body": self.__load_example()
        }

    def __load_example(self):
        with open(f'{self.__current_dir}/examples/{self.example_path}') as f:
            return f.read().strip()


event_to_response = [
    EventMatch(path="^Appointment$", method="GET", example_path="appointment/GET-success.json")
]


def process_event(request_event):
    for event in event_to_response:
        if event.match(request_event):
            return event.make_response()

    return {
        "statusCode": 404,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": "route not found"})
    }


def handler(event, context):
    return process_event(event)
