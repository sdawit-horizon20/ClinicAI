import json
import os

DB_PATH = "database/chat_history.json"

def save_chat(role, content):
    if not os.path.exists(DB_PATH):
        data = []
    else:
        with open(DB_PATH, "r") as f:
            data = json.load(f)

    data.append({"role": role, "content": content})

    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)
