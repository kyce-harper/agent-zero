from pathlib import Path

# Reads are restricted to files inside the project root.
# This blocks path traversal attacks like path="../../etc/passwd".
_ALLOWED_BASE = Path(__file__).parent.parent.resolve()

SCHEMA = {
    "name": "read_file",
    "description": (
        "Read the text contents of a file. "
        "The path must be relative to the project root, e.g. 'README.md' or 'tools/get_time.py'."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative file path from the project root.",
            },
        },
        "required": ["path"],
    },
}


def run(input: dict) -> str:
    requested = Path(input["path"])
    resolved = (_ALLOWED_BASE / requested).resolve()

    if not str(resolved).startswith(str(_ALLOWED_BASE)):
        return "Error: path escapes the project root."
    if not resolved.exists():
        return f"Error: file not found: {requested}"
    if not resolved.is_file():
        return f"Error: '{requested}' is not a file."

    try:
        return resolved.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {e}"
