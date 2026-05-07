# Sandbox Challenge

You've made it. You know how the agent loop works, how tools are structured, and how to build and register your own tools. This final challenge is open-ended — there's no single right answer.

---

## Your Challenge

Design and build a **mini agent toolkit** for a use case of your choosing.

Your toolkit must include:

1. **At least two new tools** that you write yourself
2. **A clear use case** — what problem does this agent solve?
3. **At least three test queries** that demonstrate the agent using your tools

---

## Ideas to Get You Started

Here are some directions you could go. You don't have to pick one of these — they're just starting points.

**Study Assistant Agent**
- Tool: `quiz_me` — takes a topic and returns a random quiz question (note: you'll need to either hardcode some questions or use `web_search` to generate one — it can't pull them from thin air)
- Tool: `define_term` — takes a word and returns a simple definition using a web search

**Personal Productivity Agent**
- Tool: `calculate` — takes a math expression as a string and evaluates it
- Tool: `word_count` — counts words in a block of text (you might already have this one)

**Developer Helper Agent**
- Tool: `list_files` — lists all files in the current directory
- Tool: `count_lines` — takes a filename and returns the number of lines in that file

---

## Two Things to Know Before You Build

**1. Your `run()` function should always return a string — never raise an exception.**

If something goes wrong inside a tool (file not found, bad input, network error), return a descriptive error string instead of letting it crash:

```python
def run(input: dict) -> str:
    path = input["filename"]  # pulled from what the model passed in
    try:
        with open(path) as f:
            return str(sum(1 for _ in f))  # count lines, return as string
    except FileNotFoundError:
        return f"Error: file not found: {path}"
        # Returning an error string — not raising an exception.
        # The model reads this message and tells the user what went wrong.
        # The agent keeps running. An uncaught exception would crash the whole tool call.
```

The agent will read that error string, tell you what went wrong, and keep running. If you raise an exception instead, the registry catches it — but returning a clear message yourself gives the agent something useful to work with. Open `tools/read_file.py` to see this pattern in action.

**2. The model might answer from memory instead of calling your tool.**

If you ask something the model thinks it already knows — or that sounds generic — it may skip your tool entirely and respond from its training. This is especially likely if your tool description is vague. Two ways to handle it:

- Write a more specific description. Instead of `"Lists files in the directory"`, try `"Use this to list the actual files present in the current working directory on the user's machine. Do not answer from memory."` The description is a prompt — directness helps.
- Ask the agent explicitly: `"Use the list_files tool to show me what's in this directory."` This forces the routing.

---

## What to Submit

When you're done, you should have:

- [ ] Two or more new files in the `tools/` directory
- [ ] Both tools registered in `registry.py`
- [ ] A short `SANDBOX_NOTES.md` file in the root directory that includes:
  - What your agent does
  - The names of your new tools and what they do
  - Three example queries and the responses you got

---

## Reflection Questions

Before you're done, think about these:

1. What was the hardest part of building your tools?
2. Did the agent ever call the wrong tool or misunderstand your query? What happened?
3. What would you add if you had more time?
4. How is this different from just calling those Python functions directly yourself — why does wrapping them in an agent matter?

---

*Nice work. You just built an AI agent toolkit from scratch.*
