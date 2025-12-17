import json
import os

DB_FILE = "db/chat_history.json"

def load_history():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_history(history):
    os.makedirs("db", exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
