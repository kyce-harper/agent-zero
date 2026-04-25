"""
registry.py — Tool Registry

Imports every tool module and wires their schemas and handlers together.
Adding a new tool means: create a tools/your_tool.py, then add it to _TOOL_MODULES below.

Each tool module must export one of two patterns:

  Single tool:
    SCHEMA  = { "name": ..., "description": ..., "input_schema": ... }
    def run(input: dict) -> str: ...

  Multi-tool (multiple tools in one file):
    SCHEMAS  = [ { "name": ... }, ... ]
    HANDLERS = { "tool_name": callable, ... }
"""

from tools import get_time, read_file, web_search, run_python, memory

_TOOL_MODULES = [get_time, read_file, web_search, run_python, memory]

# Collect all schemas and handlers from tool modules.
_all_schemas: list[dict] = []
_HANDLERS: dict[str, callable] = {}

for _mod in _TOOL_MODULES:
    if hasattr(_mod, "SCHEMAS"):         # multi-tool module
        _all_schemas.extend(_mod.SCHEMAS)
        _HANDLERS.update(_mod.HANDLERS)
    else:                                # single-tool module
        _all_schemas.append(_mod.SCHEMA)
        _HANDLERS[_mod.SCHEMA["name"]] = _mod.run


def _to_openai_tool(schema: dict) -> dict:
    """Convert our tool schema format to what the OpenAI API expects.

    Our format:   { "name": ..., "description": ..., "input_schema": {...} }
    OpenAI wants: { "type": "function", "function": { "name": ..., "description": ..., "parameters": {...} } }
    The JSON Schema object itself is identical — only the wrapping differs.
    """
    return {
        "type": "function",
        "function": {
            "name": schema["name"],
            "description": schema["description"],
            "parameters": schema["input_schema"],
        },
    }


OPENAI_TOOLS = [_to_openai_tool(s) for s in _all_schemas]


def dispatch_tool(name: str, input: dict) -> str:
    """Route a tool call to its handler. Returns a string result."""
    handler = _HANDLERS.get(name)
    if handler is None:
        return f"Error: unknown tool '{name}'"
    try:
        return handler(input)
    except Exception as e:
        return f"Error running tool '{name}': {e}"
