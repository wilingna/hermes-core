"""
Hermes Core — minimal implementation.
A context-routing layer that sits between two AI agents.

Usage:
    python hermes.py "<previous agent output>" "<next step goal>"
"""
import os
import sys
from openai import OpenAI

HERMES_PROMPT = """You are a Hermes Agent.
Transform the previous AI output into a clean, structured input for the next AI.

Tasks:
1. Compress (remove redundancy)
2. Normalize structure
3. Preserve core intent (do not change meaning)
4. Add constraints for the next step
5. Prepare for handoff

Output strictly in this format:
[Goal]
[Audience]
[Core Content]
[Structure]
[Constraints]
[Next Step Instruction]

Previous output:
\"\"\"{prev}\"\"\"

Next step goal:
\"\"\"{goal}\"\"\"
"""

def hermes(prev_output: str, next_goal: str, model: str = None) -> str:
    """Run a Hermes handoff between two agents."""
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Please set OPENAI_API_KEY or OPENROUTER_API_KEY")

    base_url = os.getenv("OPENAI_BASE_URL") or (
        "https://openrouter.ai/api/v1"
        if os.getenv("OPENROUTER_API_KEY") and not os.getenv("OPENAI_API_KEY")
        else "https://api.openai.com/v1"
    )
    model = model or os.getenv("HERMES_MODEL", "gpt-4o-mini")

    client = OpenAI(api_key=api_key, base_url=base_url)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are Hermes, a structured handoff agent."},
            {"role": "user", "content": HERMES_PROMPT.format(prev=prev_output, goal=next_goal)},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: python hermes.py "<previous output>" "<next step goal>"')
        sys.exit(1)
    print(hermes(sys.argv[1], sys.argv[2]))
