# In-process key-value store. State lives only for the lifetime of the process.
# This is intentionally simple — see tutorial/03_extending_the_agent.md for
# how to persist it to a JSON file or SQLite database.

_store: dict[str, str] = {}

SCHEMAS = [
    {
        "name": "memory_store",
        "description": "Save a value under a key in memory. Overwrites any existing value for that key.",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "The key to store the value under."},
                "value": {"type": "string", "description": "The value to store."},
            },
            "required": ["key", "value"],
        },
    },
    {
        "name": "memory_recall",
        "description": "Retrieve a previously stored value by key.",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "The key to look up."},
            },
            "required": ["key"],
        },
    },
]


def _store_value(input: dict) -> str:
    _store[input["key"]] = input["value"]
    return f"Stored '{input['key']}'."


def _recall_value(input: dict) -> str:
    if input["key"] not in _store:
        return f"No value found for key '{input['key']}'."
    return _store[input["key"]]


HANDLERS = {
    "memory_store": _store_value,
    "memory_recall": _recall_value,
}
