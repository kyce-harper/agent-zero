# Extending the agent

You have a working minimal agent. Here are concrete directions to take it further,
ordered roughly from easiest to hardest.

---

## 1. Persistent memory (easy)

Right now `memory_store` values are lost when `agent.py` exits. Fix this by writing the
store to a JSON file:

```python
# tools/memory.py — replace the module-level dict with file-backed storage

import json
from pathlib import Path

_STORE_PATH = Path(__file__).parent.parent / "memory_store.json"

def _load() -> dict:
    if _STORE_PATH.exists():
        return json.loads(_STORE_PATH.read_text())
    return {}

def _save(store: dict) -> None:
    _STORE_PATH.write_text(json.dumps(store, indent=2))

def _store_value(input: dict) -> str:
    store = _load()
    store[input["key"]] = input["value"]
    _save(store)
    return f"Stored '{input['key']}'."

def _recall_value(input: dict) -> str:
    store = _load()
    if input["key"] not in store:
        return f"No value found for key '{input['key']}'."
    return store[input["key"]]
```

Add `memory_store.json` to `.gitignore` so personal notes don't end up in your repo.

---

## 2. Multi-turn conversation (easy)

Currently `agent.py` takes one message and exits. To add a REPL:

```python
# agent.py — replace main() with:

def main() -> None:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")
    print("Agent-Zero  (Ctrl-C to quit)\n")
    while True:
        try:
            user_message = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not user_message:
            continue
        result = run_agent_loop(client, user_message)
        print(f"\nAgent: {result}\n")
```

Note: each call to `run_agent_loop` starts a fresh `messages` list. If you want the agent
to remember what you said two prompts ago, you need to pass the growing `messages` list
between calls — a good next exercise.

---

## 3. Streaming responses (medium)

The current loop waits silently until the model finishes. With streaming you can print tokens
as they arrive. The OpenAI SDK supports this with `stream=True`:

```python
# In loop.py, replace client.chat.completions.create(...) with:

with client.chat.completions.stream(
    model=model,
    tools=OPENAI_TOOLS,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    response = stream.get_final_completion()
```

Tool calls still happen the same way — you detect `finish_reason == "tool_calls"` on the
final message and loop. The streaming only affects the text portions.

---

## 4. System prompt (easy)

Give the model a persona or constraints by adding a `system` message at the start:

```python
# In run_agent_loop(), change the initial messages list:

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant for UC Riverside CS students. "
                   "Always explain your reasoning step by step."
    },
    {"role": "user", "content": user_message},
]
```

---

## 5. Tool call logging (easy)

Add a print statement in `_run_all_tools` to see exactly what the model is calling:

```python
def _run_all_tools(tool_calls):
    results = []
    for tc in tool_calls:
        args = json.loads(tc.function.arguments)
        print(f"  [tool] {tc.function.name}({args})")  # add this line
        output = dispatch_tool(tc.function.name, args)
        results.append(...)
    return results
```

This is useful for debugging and for understanding what the agent is actually doing.

---

## 6. Rich terminal UI (medium)

The `rich` library is already in `requirements.txt`. Here is a starting point for a
nicer interface:

```python
from rich.console import Console
from rich.panel import Panel

console = Console()

# Show a spinner while waiting for the model:
with console.status("[bold cyan]Thinking...[/]"):
    response = client.chat.completions.create(...)

# Show tool calls as panels:
for tc in msg.tool_calls or []:
    args = json.loads(tc.function.arguments)
    console.print(Panel(
        f"[bold]{tc.function.name}[/]\n{args}",
        title="Tool Call",
        border_style="yellow",
    ))
```

---

## 7. Swap to a different LLM provider (easy)

The agent uses the OpenAI SDK, which means any OpenAI-compatible provider works with a
two-line change in `agent.py`. For example, to use real OpenAI:

```python
# agent.py — remove base_url to use OpenAI directly
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
```

Other compatible providers: Together AI, Cerebras, Fireworks, Mistral, OpenRouter.
Each one just needs a different `api_key` and `base_url`.

---

## 8. Multiple agents (hard)

One agent can call another agent as a tool. Create an `agent_tool.py` that spins up a
sub-agent with a different set of tools:

```python
# tools/agent_tool.py — a "researcher" sub-agent

from loop import run_agent_loop

SCHEMA = {
    "name": "research",
    "description": "Delegate a research task to a sub-agent with web search access.",
    "input_schema": {
        "type": "object",
        "properties": {
            "task": {"type": "string", "description": "What to research"},
        },
        "required": ["task"],
    },
}

def run(input: dict) -> str:
    from openai import OpenAI
    import os
    client = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")
    return run_agent_loop(client, input["task"])
```

This is how production agent systems work — specialized sub-agents handle different parts
of a task.

---

## 9. Connect to a real API

Replace the fake weather data in the tutorial's `get_weather` example with a real call
to the Open-Meteo API (free, no key required):

```
https://api.open-meteo.com/v1/forecast?latitude=37.77&longitude=-122.42&current_weather=true
```

This is a good exercise for practicing the full tool-building loop with real external data.
