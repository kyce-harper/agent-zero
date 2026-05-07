# The Agent Loop: Inside loop.py

This is the most important file in the project. Everything else exists to support what happens here.

Open `loop.py` now and follow along.

---

## The Big Picture

The entire file does three things:

1. **Ask the model what to do next**
2. **If it wants to call a tool, run it and send the result back**
3. **If it's done, return its final answer**

That's the whole loop. Let's walk through it.

---

## Step 1: Setting Up the Conversation

When `run_agent_loop` is called, it starts with this:

```python
# The conversation is a list of dicts. Each entry has a "role" and "content".
messages = [
    {"role": "user", "content": user_message}  # start with just the user's question
]
# On each loop turn, two more types of entries get appended:
#   {"role": "assistant", ...}  — the model's response or tool request
#   {"role": "tool", ...}       — the result of a tool that ran
# The model receives the entire list on every single turn. That's its memory.
```

`messages` is a list that keeps the full conversation history. Every time something happens — the model responds, a tool runs — it gets added to this list. The model always sees the entire history on every turn.

---

## Step 2: Asking the Model

Inside the loop, the first thing that happens is a call to `_call_model()`:

```python
response = _call_model(client, model, messages)
```

That helper is defined just above `run_agent_loop` in `loop.py`. Here's what it does:

```python
def _call_model(client, model, messages):
    return client.chat.completions.create(
        model=model,               # which LLM to use
        tools=OPENAI_TOOLS,        # the menu of tools the model can choose from
        messages=messages,         # the full conversation so far
        parallel_tool_calls=False, # one tool at a time — keeps the loop easy to follow
    )
```

> **Why a helper?** The actual function in `loop.py` has a small retry inside it for a known Groq quirk. We moved it into `_call_model()` so the main loop stays readable. The logic is identical — the helper just keeps the noise out of the loop body.

This is how the model knows what tools are available. It doesn't call them itself — it just tells *us* which one it wants to use, and we run it.

---

## Step 3: Reading the Model's Decision

After the model responds, we read its decision and act on it:

```python
message = response.choices[0].message
finish_reason = response.choices[0].finish_reason  # "stop" or "tool_calls"

messages.append(message)  # always record the model's reply before branching

if finish_reason == "stop":
    return message.content or ""      # model is done — hand back its final answer

if finish_reason == "tool_calls":
    tool_results = _run_all_tools(message.tool_calls)
    messages.extend(tool_results)     # add results to history, then the loop runs again
```

Two outcomes, and only two:

- `"stop"` — the model has a final answer. We return it and exit.
- `"tool_calls"` — the model wants more information. We run the tool, add the result to `messages`, and loop again.

---

## Step 4: Running the Tool

When the model requests a tool, `_run_all_tools` handles it:

```python
def _run_all_tools(tool_calls) -> list[dict]:
    results = []
    for tool_call in tool_calls:
        args = json.loads(tool_call.function.arguments)    # arguments arrive as a JSON string — parse it
        output = dispatch_tool(tool_call.function.name, args)  # look up and run the matching Python function

        results.append({
            "role": "tool",
            "tool_call_id": tool_call.id,    # ties this result to the specific request the model made
            "content": str(output),          # everything going back to the model must be a string
        })
    return results
```

Each result gets appended to `messages` with `"role": "tool"`. The loop starts again — the model sees the result and decides what to do next.

---

## The Safety Ceiling

Notice this at the top of the loop:

```python
MAX_TURNS = 10
```

This prevents the agent from looping forever if something goes wrong. After 10 turns, it stops and returns a message saying it couldn't finish. This is a simple but important safety mechanism.

---

## Assignment 3A: Trace a Loop

1. Add a print statement inside the loop to trace what's happening. Add this right after `finish_reason = response.choices[0].finish_reason`:

```python
print(f"[Turn {turn}] finish_reason: {finish_reason}")
```

2. Now run:
```bash
python agent.py "What time is it?"
```

3. How many turns did it take? What was the finish_reason on the last turn?

4. Try a more complex query:
```bash
python agent.py "Search the web for what an LLM agent is and summarize it"
```

How many turns this time? Why do you think it took more?

---

By the end of this doc you should understand: the loop is just a `for` loop with two exit conditions — `"stop"` (done) and `"tool_calls"` (keep going). The model never runs code directly; it signals what it wants, and `loop.py` does the work. That's the whole mechanism.
