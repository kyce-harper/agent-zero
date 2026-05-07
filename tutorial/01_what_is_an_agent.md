# What is an AI agent?

A regular LLM call looks like this:

```
You: "What is 2 + 2?"
Model: "4"
```

One request, one response. The model answers from its training data and that's it.

An agent is different. It can **take actions** — call tools, read files, search the web — and
loop until it has enough information to answer properly. The model is the brain; your code is
the body.

---

## The agent loop

Here is the entire agent pattern, in pseudocode:

```
messages = [user_message]

loop:
    response = call_llm(messages, tools=available_tools)
    messages.append(response)

    if response.finish_reason == "stop":
        return response.text   # model is done

    if response.finish_reason == "tool_calls":
        for each tool_call in response:
            result = run_tool(tool_call.name, tool_call.args)
        messages.append(tool_results)
        continue  # give the model the results, let it decide what's next
```

Open `loop.py` in this project — it is almost exactly this pseudocode.

---

## finish_reason

Every response from the model includes a `finish_reason` that tells you why it stopped:

| finish_reason | Meaning |
|---------------|---------|
| `"stop"` | Model is done. Read its final text. |
| `"tool_calls"` | Model wants to call one or more tools. Run them and send results back. |
| `"length"` | Response hit the token limit. Usually means you need a higher `max_tokens`. |

In this project, `loop.py` only handles `"stop"` and `"tool_calls"`.

---

## What a tool_calls response looks like

When the model wants to call a tool, the response message has a `tool_calls` list:

```python
msg.tool_calls = [
    ChatCompletionMessageToolCall(
        id="call_abc123",
        function=Function(
            name="get_current_time",
            arguments="{}"        # always a JSON string, even when empty
        )
    )
]
```

Your loop runs the tool, then sends a `tool` role message back:

```python
{
    "role": "tool",
    "tool_call_id": "call_abc123",   # must match the id above
    "content": "UTC 2026-04-25 18:42:07"
}
```

The model reads the result and decides what to do next — either call another tool or finish.

---

## Why arguments is a JSON string

The `function.arguments` field comes back as a raw JSON string, not a dict. That's why
`loop.py` calls `json.loads(tc.function.arguments)` before passing args to your tool handler.

---

## Multi-tool calls

The model can call multiple tools in a single response. Your loop needs to handle all of them
before sending results back. In `loop.py`, `_run_all_tools()` does exactly this — it iterates
every tool call and collects all results, then `messages.extend(tool_results)` adds them all
at once.

---

## What the model cannot do

The model decides *when* to call tools and *what arguments* to pass. It cannot:
- Call a tool that is not in the `tools=` list
- Access the internet on its own (without a `web_search` tool)
- Remember anything between separate runs of `agent.py`
- Execute code on its own (without a `run_python_snippet` tool)

The agent is only as capable as the tools you give it.

---

## Why Groq?

This project uses [Groq](https://console.groq.com) as its LLM provider because it has a
genuinely free tier — no credit card required. Groq runs open-source models (Llama, Mixtral)
on custom hardware and is fast.

The code uses the `openai` Python package pointed at Groq's API endpoint. This is possible
because Groq is OpenAI-compatible — same request/response format, different URL and key.
Swapping to real OpenAI (or any other OpenAI-compatible provider) is a two-line change in
`agent.py`.
