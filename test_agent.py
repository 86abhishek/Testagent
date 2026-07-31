import json
import os
from typing import Any
from anyio import Path
from dotenv import load_dotenv
from langchain_githubcopilot_chat import ChatGithubCopilot
load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

DEFAULT_DUMMY_ITEMS = [
    {"id": 1, "name": "Apple"},
    {"id": 2, "name": "Banana"},
    {"id": 3, "name": "Cherry"},
]

def generate_dummy_items() -> list[dict[str, Any]]:
    """Generate dummy item data, preferring an LLM when available."""
    if ChatGithubCopilot is None:
        return DEFAULT_DUMMY_ITEMS.copy()

    

    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        return DEFAULT_DUMMY_ITEMS.copy()

    try:
        llm = ChatGithubCopilot(
            model="Auto", 
            base_url="https://api.githubcopilot.com",
            api_key=github_token,
            temperature=0.2
        )
        prompt = "Return ONLY a JSON array of objects with fields 'id' and 'name'. Create exactly 3 dummy items for a simple inventory list."
        response = llm.invoke(prompt).content
        if isinstance(response, str):
            text = response.strip()
            if text.startswith("```"):
                text = text.strip("`").strip()
                if text.lower().startswith("json"):
                    text = text[4:].strip()
            parsed = json.loads(text)
            if isinstance(parsed, list) and all(isinstance(item, dict) for item in parsed):
                return parsed
    except Exception as exc:  # pragma: no cover - runtime fallback
        print(f"LLM generation failed: {exc}")

    return DEFAULT_DUMMY_ITEMS.copy()


try:
    test = generate_dummy_items()
    for item in test:
        for key, value in item.items():
            print(f"{key}: {value}")
except ImportError:  # pragma: no cover - handled gracefully in local environments
    ChatGithubCopilot = None
    HumanMessage = None



