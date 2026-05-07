"""
loop.py — The Agent Loop

This is the core of the framework. Read this file first.

The loop does three things, over and over:
  1. Ask the model what to do next.
  2. If it wants to call a tool, run it and send the result back.
  3. If it's done, return its final text response.

That's it. Everything else in this project exists to support this loop.
"""

import json
from openai import OpenAI
from registry import OPENAI_TOOLS, dispatch_tool

# Ordered by preference for tool-use reliability on Groq's free tier.
# The agent picks the first one that's available on your account.
_PREFERRED_MODELS = [
    "llama-3.1-70b-versatile",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

MAX_TURNS = 10  # safety ceiling — prevents runaway loops on bad tool output


def pick_model(client: OpenAI) -> str:
    available = {m.id for m in client.models.list()}
    for model in _PREFERRED_MODELS:
        if model in available:
            return model
    raise RuntimeError(
        "No supported model found. Check https://console.groq.com/docs/models "
        "and add a model name to _PREFERRED_MODELS in loop.py."
    )


def _call_model(client: OpenAI, model: str, messages: list) -> object:
    """Ask the model what to do next. Retries once on known Groq tool-call failures."""
    for attempt in range(2):
        try:
            return client.chat.completions.create(
                model=model,
                tools=OPENAI_TOOLS,
                messages=messages,
                parallel_tool_calls=False,
            )
        except Exception as e:
            if attempt == 0 and "tool_use_failed" in str(e):
                continue
            raise


def run_agent_loop(client: OpenAI, user_message: str) -> str:
    """
    Run the agent loop for a single user message.
    Returns the agent's final text response.
    """
    model = pick_model(client)
    messages = [{"role": "user", "content": user_message}]

    for turn in range(MAX_TURNS):
        response = _call_model(client, model, messages)

        message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        messages.append(message)

        if finish_reason == "stop":
            return message.content or ""

        if finish_reason == "tool_calls":
            tool_results = _run_all_tools(message.tool_calls)
            messages.extend(tool_results)

    return "Reached maximum turns without a final answer."


def _run_all_tools(tool_calls) -> list[dict]:
    """Execute every tool call and return a list of tool result messages."""
    results = []
    for tool_call in tool_calls:
        args = json.loads(tool_call.function.arguments)
        output = dispatch_tool(tool_call.function.name, args)
        results.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(output),
        })
    return results
