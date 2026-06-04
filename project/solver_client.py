import requests
import datetime

def serialize(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj

def clean_state(state):
    cleaned = {}

    for k, v in state.items():
        cleaned[k] = {}

        for key, value in v.items():
            cleaned[k][key] = serialize(value)

    return cleaned


def get_plan(state):

    url = "http://localhost:8000/solve"

    safe_state = clean_state(state)

    response = requests.post(url, json={"state": safe_state})

    return response.json()
