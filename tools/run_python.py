import subprocess
import sys

# SECURITY WARNING: This executes arbitrary Python code in a subprocess.
# Never expose this tool to untrusted input outside of educational/local use.
# The 5-second timeout prevents infinite loops; stdout is capped at 1000 chars.

SCHEMA = {
    "name": "run_python_snippet",
    "description": (
        "Execute a short Python code snippet and return its stdout output. "
        "Useful for math, data transformations, or quick experiments. "
        "Has a 5-second timeout. Prints to stdout to return results."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Python source code to execute. Use print() to return values.",
            },
        },
        "required": ["code"],
    },
}


def run(input: dict) -> str:
    code: str = input["code"]
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        return "Error: code execution timed out after 5 seconds."

    if result.returncode != 0:
        return f"Error:\n{result.stderr[:500]}"
    return result.stdout[:1000] or "(no output)"
