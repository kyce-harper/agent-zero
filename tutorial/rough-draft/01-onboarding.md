# Onboarding: Get Agent-Zero Running

Welcome to Agent-Zero. By the end of this doc you'll have the project running on your machine and have sent your first message to the agent.

## What You'll Need

- Python 3.8 or higher
- A terminal (macOS/Linux) or Command Prompt / PowerShell (Windows)
- A free Groq API key (takes about 2 minutes to get)

---

## Step 1: Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/kyce-harper/agent-zero.git
cd agent-zero
```

This downloads the full project to your machine and moves you into the folder.

---

## Step 2: Install Dependencies

Agent-Zero needs two Python packages:

```bash
pip install openai ddgs
```

- `openai` — the SDK we use to talk to the AI model. Groq speaks the same API language as OpenAI, so we borrow their SDK — you don't need an OpenAI account.
- `ddgs` — powers the web search tool using DuckDuckGo

> **Using a virtual environment?** If you have multiple Python projects on your machine, it's worth isolating this one: `python -m venv venv && source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows). Run this before `pip install`.

---

## Step 3: Get Your Free Groq API Key

1. Go to [https://console.groq.com](https://console.groq.com) and sign up for a free account.
2. Navigate to **API Keys** in the sidebar.
3. Click **Create API Key**, give it a name, and copy it.

Now set it as an environment variable in your terminal:

**macOS / Linux:**
```bash
export GROQ_API_KEY=your_key_here
```

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_key_here"
```

> **Note:** You'll need to run this command every time you open a new terminal window. To make it permanent, add it to your shell's config file (e.g. `~/.zshrc` or `~/.bashrc`).

---

## Step 4: Run Your First Agent Command

```bash
python agent.py "What time is it?"
```

You should see output that looks something like this:

```
Agent: The current UTC time is 2025-06-16 14:32:05.
```

Try another one:

```bash
python agent.py "Search the web for the latest news about AI agents"
```

If you see a response, you're all set. Move on to the next doc.

---

## Troubleshooting

**"GROQ_API_KEY environment variable is not set"** — You haven't exported your key yet. Go back to Step 3.

**"No module named 'openai'"** — Run `pip install openai ddgs` again.

**"No supported model found"** — Your Groq account may not have access to the models listed in `loop.py`. Check [https://console.groq.com/docs/models](https://console.groq.com/docs/models) for available models.

---

By the end of this doc you should have: the project cloned, dependencies installed, an API key set, and a working agent response in your terminal. If all three are true, you're ready for Doc 2.
