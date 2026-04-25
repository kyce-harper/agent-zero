# Adding a new tool

This walkthrough adds a `get_weather` tool that returns a (fake) weather report.
By the end, the agent will be able to answer "What's the weather in San Francisco?"

---

## Step 1: Create the tool file

Create `tools/weather.py`:

```python
# tools/weather.py

SCHEMA = {
    "name": "get_weather",
    "description": (
        "Get the current weather for a city. "
        "Returns temperature and conditions."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city name, e.g. 'San Francisco'.",
            },
        },
        "required": ["city"],
    },
}


def run(input: dict) -> str:
    city = input["city"]
    # Replace this with a real weather API call if you want.
    return f"Weather in {city}: 68°F, partly cloudy."
```

That's it. The file has two things:
- `SCHEMA` — the JSON description of the tool that gets sent to the model
- `run(input)` — the function that gets called when the model uses the tool

---

## Step 2: Register it in registry.py

Open `registry.py` and add your module to the imports and `_TOOL_MODULES` list:

```python
# Before
from tools import get_time, read_file, web_search, run_python, memory

_TOOL_MODULES = [get_time, read_file, web_search, run_python, memory]

# After
from tools import get_time, read_file, web_search, run_python, memory, weather

_TOOL_MODULES = [get_time, read_file, web_search, run_python, memory, weather]
```

That is the only change needed. The registry loop handles the rest automatically.

---

## Step 3: Test it

```bash
python agent.py "What's the weather in Tokyo?"
```

Expected output (approximately):
```
Agent: The weather in Tokyo is currently 68°F with partly cloudy skies.
```

---

## The tool schema in detail

```python
SCHEMA = {
    "name": "get_weather",          # What the model calls to invoke it (must be unique)
    "description": "...",           # The model reads this to decide WHEN to use the tool.
                                    # Write it as a sentence that completes:
                                    # "Use this tool when you need to..."
    "input_schema": {
        "type": "object",           # Always "object"
        "properties": {
            "city": {
                "type": "string",   # JSON Schema type: string, number, boolean, array, object
                "description": "...", # The model reads this to know what value to pass
            },
        },
        "required": ["city"],       # List of required parameter names
    },
}
```

Tips for writing good descriptions:
- Be specific about what the tool returns, not just what it does
- Mention any limitations ("only works for US cities", "returns mock data")
- If a parameter has a specific format, say so ("e.g. 'San Francisco, CA'")

---

## Tools with no parameters

If your tool takes no input (like `get_current_time`):

```python
"input_schema": {
    "type": "object",
    "properties": {},
    "required": [],
}
```

The `run` function still receives `input: dict`, it will just be empty (`{}`).

---

## Tools with multiple parameters

```python
"input_schema": {
    "type": "object",
    "properties": {
        "city": {"type": "string", "description": "City name"},
        "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],  # enum constrains the value
            "description": "Temperature unit",
        },
    },
    "required": ["city"],  # unit is optional
},
```

Access them in `run`:
```python
def run(input: dict) -> str:
    city = input["city"]
    unit = input.get("unit", "fahrenheit")  # use .get() for optional params
    ...
```

---

## Multi-tool files

If you want two related tools in one file (like `memory.py` does for store and recall),
export `SCHEMAS` (a list) and `HANDLERS` (a dict) instead of `SCHEMA` and `run`:

```python
SCHEMAS = [
    {"name": "tool_a", ...},
    {"name": "tool_b", ...},
]

HANDLERS = {
    "tool_a": lambda input: "result from a",
    "tool_b": lambda input: "result from b",
}
```

The registry checks for `SCHEMAS` vs `SCHEMA` and handles both patterns automatically.
