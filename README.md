# agent-zero

A minimal AI agent framework built for learning. This project strips an agent down to exactly
two things: a loop that talks to an LLM, and a set of tools the model can call. No framework
magic, no hidden abstractions — just Python you can read top-to-bottom.

Built for UC Riverside CS 180. Inspired by Claude Code.

---

## What does this do?

You send a message. The agent figures out what tools it needs, calls them, and responds.

```
$ python agent.py "What is 17 * 23, and what time is it right now?"

Agent: 17 × 23 = 391. The current UTC time is 2026-04-25 18:42:07.
```

Behind that response, the agent:
1. Asked the model what to do
2. The model called `run_python_snippet` to compute 17 * 23
3. The model called `get_current_time` to get the time
4. The model combined both results into a final answer

---

## How agents work

The entire framework is this loop:

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
Your job is to define the tools and keep the loop running.

See `loop.py` — it's ~50 lines and does everything described above.

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
export GROQ_API_KEY=your_key_here

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
├── loop.py       THE loop. Read this first — it's the whole framework.
├── registry.py   Wires tool files to the loop. Add new tools here.
└── tools/
    ├── get_time.py     Tool 1: get_current_time — no params, stdlib only
    ├── read_file.py    Tool 2: read_file — reads files in this directory
    ├── web_search.py   Tool 3: web_search — DuckDuckGo, no API key needed
    ├── run_python.py   Tool 4: run_python_snippet — runs Python code
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

The short version: create a file in `tools/`, export a `SCHEMA` dict and a `run()` function,
then add your module to `_TOOL_MODULES` in `registry.py`. That's it.

---

## How the model is selected

The agent automatically picks the best available model from your Groq account. You never
need to set a model name — it checks what's available and chooses from a priority list in
`loop.py`. If Groq adds or removes models, it still works.

---

## Security note

`run_python_snippet` executes real Python code in a subprocess. It is intentionally included
as a teaching tool to show how agents can take real actions — but **never expose it to untrusted
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
rich>=13.7.0     Terminal formatting (used in stretch goal UI)
```
