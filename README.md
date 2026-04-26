# Agent-Zero

A minimal AI agent framework built for learning. This project strips the coding agent down to exactly two things: a loop that talks to an LLM, and a set of tools the model can call.

---

## How does this work?

You send a message. The agent figures out what tools it needs, calls them, and responds. You cant secure a screw with a hammer, so calling the right tools are important. Take this chat for example.

```
You: "What time is it right now?"

Agent: The current UTC time is 2026-04-25 18:42:07.
```

Behind that response, the agent:
1. Asked the model what to do
2. The model called a usefull tool for the prompt: `get_current_time` to get the time
3. The model put its results into the final answer

---

---

## Full tutorial directions

Navigate the `tutorial` folder for a step by step guide on how to setup your sandbox. I am planning a youtube series soon and will link them as soon as those are made. 

---

## How agents work

Visualize the framework like this:

```
User message
     |
     v
  LLM API  <-------+
     |              |
  tool_calls?  --yes-+  (run the tool, send result back)
     |
    no (stop)
     |
     v
Final response
```

The model decides when to call tools, which tools to call, and what arguments to pass.
Your job is to define the tools and keep the loop running. Think of yourself now as supplying the resources and creating a plan for the agent to execute using the tools you provide. Once again you cant expect any screws to be secured if you give your employee a hammer.

See `loop.py` - it's ~50 lines and does everything described above with comments.

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/your-username/agent-zero
cd agent-zero

# 2. Install dependencies
pip install -r requirements.txt

# 3. Get a free API key at https://console.groq.com
#    Sign in with Google → API Keys → Create API Key. No credit card needed.

# 4. Run
python agent.py "What time is it?"
python agent.py "Search the web for Python 3.12 new features"
python agent.py "Remember that my name is Alex, then greet me by name"
```

---

## Project structure

```
agent-zero/
├── agent.py      Entry point. Parses your message, calls run_agent_loop().
├── loop.py       THE loop. Read this first: it's the whole framework.
├── registry.py   Wires tool files to the loop. Add new tools here.
└── tools/
    ├── get_time.py     Tool 1: get_current_time - no params, stdlib only
    ├── read_file.py    Tool 2: read_file - reads files in this directory
    ├── web_search.py   Tool 3: web_search - DuckDuckGo, no API key needed
    ├── run_python.py   Tool 4: run_python_snippet - runs Python code
    └── memory.py       Tool 5: memory_store + memory_recall
```

Start by reading `loop.py`, then `registry.py`, then any tool file. The whole codebase
is under 200 lines of Python.

---

## The five example tools

| Tool | What it does | Teaches |
|------|-------------|---------|
| `get_current_time` | Returns current UTC time | Basic tool shape |
| `read_file` | Reads a file in the project | Parameters + path safety |
| `web_search` | DuckDuckGo search (free) | External HTTP calls |
| `run_python_snippet` | Runs Python code in a subprocess | Side effects + timeouts |
| `memory_store` / `memory_recall` | In-memory key-value store | Shared state, two tools in one file |

---

## Adding your own tool

See [tutorial/02_adding_a_tool.md](tutorial/02_adding_a_tool.md) for a step-by-step walkthrough.

---

## Why Groq?
The goal of this repo is to educate people on the agent loop. Groq is the quickest way for anyone to create a free account (No card required) and start to play around with the agent loop (Its 100% free) and uses different models. It also is compatible with OpenAI SDK so for people who have api credits with them also feel free to use OpenAI also.

The agent automatically picks the best available model from your Groq account. You never
need to set a model name, it checks what's available and chooses from a priority list in
`loop.py`. If Groq adds or removes models, it still works. Dont worry aboutt this to much if your goal is just to learn more about agents but you can read more about this in `loop.py`.

---

## Security note

`run_python_snippet` executes real Python code in a subprocess. It is intentionally included
as a teaching tool to show how agents can take real actions but **never expose it to untrusted
input**. The 5-second timeout prevents infinite loops, but there is no sandbox. Treat it like
`eval()`.

---

## Known limitations

- **Memory is in-process.** `memory_store` values are lost when you restart. See
  [tutorial/03_extending_the_agent.md](tutorial/03_extending_the_agent.md) for how to persist them.
- **No streaming.** Responses appear all at once when the loop finishes. The OpenAI SDK
  supports streaming; wiring it up is a good extension exercise.
- **DuckDuckGo rate limits.** If you run many searches quickly, results may be empty.
- **Single conversation.** Each run of `agent.py` starts fresh. There is no conversation history
  across runs (yet).

---

## Dependencies

```
openai>=1.0.0    OpenAI-compatible SDK — works with Groq (and real OpenAI) out of the box
ddgs>=6.0.0      DuckDuckGo search, no API key required
```

