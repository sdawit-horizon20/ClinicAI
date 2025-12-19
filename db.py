import json
from pathlib import Path

DB_FILE = Path(__file__).parent.parent / "03_DATABASE/01_chat_history.json"

def save_chat(user_input: str, ai_response: str):
    """Append chat to JSON database"""
    if DB_FILE.exists():
        with open(DB_FILE, "r") as f:
            chats = json.load(f)
    else:
        chats = []

    chats.append({"user": user_input, "ai": ai_response})

    with open(DB_FILE, "w") as f:
        json.dump(chats, f, indent=4)
