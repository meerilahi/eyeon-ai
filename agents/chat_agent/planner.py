# agents/chat_agent/planner.py

from llms.language_model import call_llm
from pathlib import Path

PROMPT_FILE = Path("llms/prompts/chat_agent_prompt.txt").read_text()

def parse_event_from_instruction(user_input: str) -> dict:
    prompt = f"{PROMPT_FILE}\n\nUser: {user_input}\nAI:"
    response = call_llm(prompt)
    try:
        event = eval(response.strip())  # Use json.loads() in production
        return event
    except Exception as e:
        raise ValueError(f"Invalid LLM response: {response}") from e
