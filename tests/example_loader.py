import os
import json

current_directory = os.path.dirname(os.path.realpath(__file__))


def load_example(path: str):
    with open(f"{current_directory}/../sandbox/src/routes/examples/{path}") as f:
        if path.endswith("json"):
            return json.load(f)
        else:
            return f.read().strip()
