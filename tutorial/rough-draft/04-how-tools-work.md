# How Tools Work

The agent can only do things because of tools. This doc walks through exactly how they're structured, registered, and called.

---

## What a Tool Looks Like

Open `tools/get_time.py`:

```python
from datetime import datetime, timezone

SCHEMA = {
    "name": "get_current_time",       # the name the model calls to request this tool
    "description": (
        "Returns the current UTC date and time as a formatted string."
        # The model reads this to decide WHEN to call this tool.
        # Treat it like the tool's job posting — be specific.
    ),
    "input_schema": {
        "type": "object",
        "properties": {},  # no inputs — this tool needs nothing from the model to run
        "required": [],
    },
}

def run(input: dict) -> str:  # always takes a dict, always returns a string
    now = datetime.now(timezone.utc)
    return now.strftime("UTC %Y-%m-%d %H:%M:%S")
```

Every tool in this project has two parts:

1. **`SCHEMA`** — tells the model what the tool is called, what it does, and what inputs it expects
2. **`run(input)`** — the actual Python function that does the work

The model reads the schema to decide *whether* to use the tool. Python runs `run()` to actually execute it.

> **Important:** The `description` field is not just documentation — it's essentially a prompt. The model reads it to decide when to call this tool and what it does. A vague description leads to a tool the model ignores or misuses. Write descriptions like you're giving instructions to a smart person who has no other context.

## How Tools Get Registered

Open `registry.py`. This is where all the tools get wired together.

```python
from tools import get_time, read_file, web_search, run_python, memory

_TOOL_MODULES = [get_time, read_file, web_search, run_python, memory]
```

The registry loops through every module, grabs its `SCHEMA` and `run` function, and builds two things:

- `OPENAI_TOOLS` — the list of schemas passed to the model
- `_HANDLERS` — a dictionary mapping tool names to their `run` functions

When the model says "call `get_current_time`", `dispatch_tool` looks up `get_current_time` in `_HANDLERS` and runs it.

> **What about `parameters`?** If you've seen OpenAI's documentation, you may have noticed they use `"parameters"` where we use `"input_schema"`. Both refer to the same JSON Schema object. The registry's `_to_openai_tool()` function handles the rename automatically before sending anything to the API. Always use `input_schema` in your tool files — the registry takes care of the rest.

---

## A More Complex Tool: web_search

Now open `tools/web_search.py`:

```python
SCHEMA = {
    "name": "web_search",
    "description": (
        "Search the web using DuckDuckGo. "
        "Returns the top 3 results with title, URL, and a short snippet. "
        "Use this for current events, facts, or anything that requires up-to-date information."
        # Specific and action-oriented — the model knows exactly when to reach for this.
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query string.",  # the model fills this in
            },
        },
        "required": ["query"],  # the model must provide this field — or the tool won't run
    },
}

def run(input: dict) -> str:
    from ddgs import DDGS
    query: str = input["query"]  # pull out what the model decided to search for
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=3):
            results.append(
                f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}"
            )
    return "\n---\n".join(results)  # one string back to the model, results separated by ---
```

Notice that this tool takes an input — `query`. The model fills this in based on the user's request. When you ask "search for AI agents", the model sets `query = "AI agents"` and the tool runs with that.

---

## Assignment 4A: Read a Tool, Predict Its Behavior

1. Open `tools/read_file.py` and read through the schema and `run` function.
2. Without running it, answer these questions:
   - What input does this tool take?
   - What does it return?
   - What do you think would happen if you asked the agent: `python agent.py "Read README.md and summarize it"`?
3. Now run that command. Were you right?

---

## Assignment 4B: Trace a Tool Call

> **Before you start:** If you added the print statement from Assignment 3A, remove it from `loop.py` first. Otherwise you'll have overlapping output that's hard to read.

Add this print statement to `_run_all_tools` in `loop.py`, right before the `results.append(...)` line:

```python
print(f"[Tool] Called: {tool_call.function.name} with args: {args}")
print(f"[Tool] Result: {output}")
```

Run a few queries and watch what gets printed. Try:

```bash
python agent.py "What time is it?"
python agent.py "Search the web for Python tutorials"
python agent.py "Read README.md and tell me what this project is"
```

---

By the end of this doc you should understand: every tool is a schema plus a `run` function. The schema is what the model reads (and the `description` is the most important part). The `run` function is what Python executes. The registry wires them together so you never have to touch `loop.py` when adding a new tool.
