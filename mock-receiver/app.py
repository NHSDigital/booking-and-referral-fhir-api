import json
import os
import re
from dataclasses import dataclass

current_directory = os.path.dirname(os.path.realpath(__file__))


@dataclass
class EventMatch:
    path: str
    method: str
    example_path: str

    def match(self, e) -> bool:
        return re.match(self.path, e["pathParameters"]["proxy"]) and self.method == e["httpMethod"]


routes_to_examples = [
    EventMatch(path="^Appointment$", method="GET", example_path="appointment/GET-success.json")
]


def process_event(event):
    for route in routes_to_examples:
        if route.match(event):
            example = load_example(route.example_path)
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps(example)
            }

    return {
        "statusCode": 404,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": "route not found"})
    }


def load_example(path: str):
    with open(f'{current_directory}/examples/{path}') as f:
        if path.endswith('json'):
            return json.load(f)
        else:
            return f.read().strip()


def handler(event, context):
    print(json.dumps(event))
    return process_event(event)
