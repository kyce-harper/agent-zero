from datetime import datetime, timezone

SCHEMA = {
    "name": "get_current_time",
    "description": "Returns the current UTC date and time as a formatted string.",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def run(input: dict) -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("UTC %Y-%m-%d %H:%M:%S")
