# What Is an Agent?

You've probably used ChatGPT or a similar AI chatbot before. You type something, it responds. Simple.

An **agent** is different. This doc explains how.

---

## The Difference Between a Chatbot and an Agent

A standard **LLM** (Large Language Model) like ChatGPT does one thing: it takes text in and produces text out. It has no ability to actually *do* anything in the real world. It can't check the current time, search the web, or read a file on your computer. It can only generate text based on what it already knows.

An agent wraps an LLM with a **loop** and **tools**. Now the model can:

- Decide it needs more information
- Call a tool to get that information
- Use the result to form a better answer
- Repeat as needed until it's done

Here's the simplest way to think about it:

| | Chatbot (plain LLM) | Agent |
|---|---|---|
| Gets input | ✅ | ✅ |
| Produces text | ✅ | ✅ |
| Can take actions | ❌ | ✅ |
| Can use tools | ❌ | ✅ |
| Can loop until done | ❌ | ✅ |

---

## The Basic Agent Loop

Every agent — no matter how complex — runs some version of this loop:

```
1. User sends a message
2. LLM decides what to do next
   - If it has enough info → respond and stop
   - If it needs a tool → call the tool
3. Tool runs and returns a result
4. LLM sees the result and decides what to do next
5. Repeat from step 2
```

In Agent-Zero, this loop lives in `loop.py`. You'll dig into it in the next doc.

---

## A Real Example

Say you ask: **"What time is it?"**

A plain LLM would say something like: *"I don't have access to real-time information, so I can't tell you the current time."*

An agent does this:

1. Model receives your question
2. Model decides to call the `get_current_time` tool
3. The tool runs and returns `"UTC 2025-06-16 14:32:05"`
4. Model sees the result and responds: *"The current UTC time is 2:32 PM on June 16th, 2025."*

Same model. Completely different result — because of the loop and the tool.

---

## Assignment 2A: Spot the Difference

1. Run this command and note the response:
```bash
python agent.py "What is the capital of France?"
```

2. Now run this one:
```bash
python agent.py "What time is it right now?"
```

3. Notice that the first question the model could answer from memory. The second required a tool. You can't see which tool it used yet — that's exactly what Doc 3 covers. For now, just observe that the responses feel different: one is instant recall, one is live information.

---

By the end of this doc you should understand: an agent is an LLM plus a loop plus tools. The model doesn't take actions itself — it requests them, and our code runs them. That mental model is the foundation for everything that follows.
