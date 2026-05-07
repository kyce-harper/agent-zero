# Agent-Zero

A minimal AI agent framework built for learning. This project strips the agent down to exactly two things: a loop that talks to an LLM, and a set of tools the model can call.

---

## How it works

You send a message. The agent figures out which tools it needs, calls them, and responds. The model decides when to use tools — your job is to define them.

```
You: "What time is it right now?"

Agent: The current UTC time is 2026-04-25 18:42:07.
```

Behind that response, the agent:
1. Sent your question to the model
2. The model requested the `get_current_time` tool to get the live time
3. The model used the result to write its final answer

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/kyce-harper/agent-zero
cd agent-zero

# 2. Install dependencies
pip install -r requirements.txt

# 3. Get a free API key at https://console.groq.com
#    Sign in → API Keys → Create API Key. No credit card needed.

# 4. Set your key
export GROQ_API_KEY=your_key_here

# 5. Run
python agent.py "What time is it?"
python agent.py "Search the web for Python 3.12 new features"
python agent.py "Remember that my name is Alex, then greet me by name"
```

---

## Tutorial

The `tutorial/` folder contains a six-part guided series:

| Doc | Topic |
|-----|-------|
| `01-onboarding.md` | Get the project running |
| `02-what-is-an-agent.md` | Chatbots vs. agents — the key difference |
| `03-the-agent-loop.md` | Inside `loop.py` — how the loop works |
| `04-how-tools-work.md` | Tool structure, registration, and the schema |
| `05-your-first-tool.md` | Build and register a tool from scratch |
| `06-sandbox-challenge.md` | Open-ended project: design your own toolkit |

Start with `01-onboarding.md`.

---

## How agents work

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

The model decides when to call tools, which tools to call, and what arguments to pass. Your job is to define the tools and keep the loop running.

See `loop.py` — it's under 100 lines and does everything described above.

---

## Project structure

```
agent-zero/
├── agent.py      Entry point. Parses your message, calls run_agent_loop().
├── loop.py       The loop. Read this first: it's the whole framework.
├── registry.py   Wires tool files to the loop. Add new tools here.
└── tools/
    ├── get_time.py     Tool 1: get_current_time — no params, stdlib only
    ├── read_file.py    Tool 2: read_file — reads files in this directory
    ├── web_search.py   Tool 3: web_search — DuckDuckGo, no API key needed
    ├── run_python.py   Tool 4: run_python_snippet — runs Python code
    └── memory.py       Tool 5: memory_store + memory_recall
```

Start by reading `loop.py`, then `registry.py`, then any tool file.

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

## Why Groq?

The goal of this repo is to teach the agent loop. Groq is the fastest way to get started — free account, no credit card required, and it's OpenAI SDK-compatible so the same code works if you already have OpenAI credits.

The agent automatically picks the best available model from your Groq account. You never need to set a model name manually. You can read more about how this works in `loop.py`.

---

## Roadmap

- [ ] File editing and creation tools
- [ ] Code generation + test-bench workflow example
- [ ] Persistent memory (currently resets on restart)
- [ ] Streaming output support

---

## Security note

`run_python_snippet` executes real Python code in a subprocess. It is intentionally included
as a teaching tool to show how agents can take real actions, but **never expose it to untrusted
input**. The 5-second timeout prevents infinite loops, but there is no sandbox. Treat it like
`eval()`.

---

## Known limitations

- **Memory is in-process.** `memory_store` values are lost when you restart.
- **No streaming.** Responses appear all at once when the loop finishes.
- **DuckDuckGo rate limits.** If you run many searches quickly, results may be empty.
- **Single conversation.** Each run of `agent.py` starts fresh with no history from prior runs.

---

## Dependencies

```
openai>=1.0.0    OpenAI-compatible SDK — works with Groq (and real OpenAI) out of the box
ddgs>=6.0.0      DuckDuckGo search, no API key required
```
