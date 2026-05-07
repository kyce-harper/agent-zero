# Your First Tool

You've seen how tools work. Now you're going to build one from scratch and plug it into the agent.

---

## What You're Building

You'll create a simple tool called `get_random_number` that returns a random integer between two numbers the user specifies.

---

## Step 1: Create the Tool File

Create a new file at `tools/random_number.py` and add the following:

```python
import random

SCHEMA = {
    "name": "get_random_number",  # the model uses this name to call the tool
    "description": (
        "Returns a random integer between min_value and max_value (inclusive). "
        "Use this when the user asks for a random number."
        # Clear trigger phrase: "when the user asks for a random number."
        # The model matches this against the user's intent to decide whether to call it.
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "min_value": {
                "type": "integer",           # the model will only pass an integer here
                "description": "The minimum value (inclusive).",
            },
            "max_value": {
                "type": "integer",
                "description": "The maximum value (inclusive).",
            },
        },
        "required": ["min_value", "max_value"],  # the model must provide both fields
    },
}

def run(input: dict) -> str:
    min_val = input["min_value"]  # the model chose these values based on what the user asked
    max_val = input["max_value"]
    result = random.randint(min_val, max_val)
    return f"Random number between {min_val} and {max_val}: {result}"
    # always a string — the model reads this and weaves it into its reply to the user
```

---

## Step 2: Register the Tool

Open `registry.py`. Find this line:

```python
from tools import get_time, read_file, web_search, run_python, memory
```

Add your new tool:

```python
from tools import get_time, read_file, web_search, run_python, memory, random_number
```

Then find:

```python
_TOOL_MODULES = [get_time, read_file, web_search, run_python, memory]
```

And add it:

```python
_TOOL_MODULES = [get_time, read_file, web_search, run_python, memory, random_number]
```

That's it. The registry handles the rest automatically.

---

## Step 3: Test It

```bash
python agent.py "Give me a random number between 1 and 100"
```

You should see the agent call your new tool and return a random number.

Try a few more:

```bash
python agent.py "Pick a random number between 1 and 6 like rolling a dice"
python agent.py "Give me 3 random numbers between 10 and 50"
```

---

## Assignment 5A: Build Your Own Tool

Now build a tool yourself — no starter code this time.

**Your task:** Create a tool called `word_count` that takes a string of text and returns the number of words in it.

Requirements:
- Create `tools/word_count.py`
- The tool should accept one input: `text` (a string)
- It should return a string like: `"Word count: 42"`
- Register it in `registry.py`
- Test it by asking the agent: `python agent.py "How many words are in 'The quick brown fox jumps over the lazy dog'?"`

**Hint:** In Python, `len("hello world".split())` returns `2`.

---

## Assignment 5B: Stretch Goal

Modify your `word_count` tool to also return the character count alongside the word count. The output might look like:

```
Words: 9 | Characters: 44
```

---

By the end of this doc you should be able to: create a tool file, write a valid schema with a clear description, implement `run()`, register the tool, and verify the agent picks it up. That's the full workflow for extending any agent built on this pattern.
