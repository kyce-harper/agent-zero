"""
agent.py — Entry Point

Run the agent from the command line:

  python agent.py "What time is it?"
  python agent.py "Read README.md and summarize it"
  python agent.py   # prompts you interactively

Set your API key first:
  export GROQ_API_KEY=your_key_here

Get a free key at: https://console.groq.com
"""

import os
import sys

from openai import OpenAI

from loop import run_agent_loop

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


def main() -> None:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable is not set.")
        print("Get a free key at https://console.groq.com")
        print("Then run: export GROQ_API_KEY=your_key_here")
        sys.exit(1)

    # Groq is OpenAI-compatible — same SDK, different base_url and key.
    client = OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)

    if len(sys.argv) > 1:
        user_message = " ".join(sys.argv[1:])
    else:
        user_message = input("You: ").strip()
        if not user_message:
            print("No message provided.")
            sys.exit(1)

    print()
    result = run_agent_loop(client, user_message)
    print(f"Agent: {result}")


if __name__ == "__main__":
    main()
