"""
HR Agent powered by Grok (xAI)
Single-file, minimal, extensible.

Author: You
"""

import os
import requests
import json

# ==============================
# CONFIG
# ==============================

GROK_API_KEY = os.getenv("GROK_API_KEY")  # export GROK_API_KEY="your_key"
GROK_API_URL = "https://api.x.ai/v1/chat/completions"
MODEL_NAME = "grok-2"

# ==============================
# HR SYSTEM PROMPT
# ==============================

HR_SYSTEM_PROMPT = """
You are an experienced HR professional and talent strategist.

You specialize in:
- Candidate screening
- Interview questions
- Hiring decisions
- HR policies
- Performance reviews
- Workplace communication

Your tone is professional, unbiased, structured, and practical.
You think step-by-step before answering.
"""

# ==============================
# CORE HR AGENT
# ==============================

class HRAgent:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("GROK_API_KEY not set")
        self.api_key = api_key

    def ask(self, user_query: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": HR_SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ],
            "temperature": 0.4
        }

        response = requests.post(
            GROK_API_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=60
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Grok API Error {response.status_code}: {response.text}"
            )

        data = response.json()
        return data["choices"][0]["message"]["content"]


# ==============================
# CLI INTERFACE
# ==============================

def main():
    print("\n🧑‍💼 HR Agent (powered by Grok)")
    print("Type 'exit' to quit.\n")

    agent = HRAgent(GROK_API_KEY)

    while True:
        query = input("HR Query ➜ ").strip()
        if query.lower() in {"exit", "quit"}:
            print("👋 HR Agent signing off.")
            break

        try:
            answer = agent.ask(query)
            print("\n📋 HR Response:\n")
            print(answer)
            print("\n" + "-" * 50 + "\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")


# ==============================
# ENTRY POINT
# ==============================

if __name__ == "__main__":
    main()