import os
import json
from openai import OpenAI

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "chat_history.json")


def load_history():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def get_ai_response(user_message):
    history = load_history()

    messages = [
        {"role": "system", "content": "You are ClinicAI, a helpful medical assistant."}
    ]

    for h in history[-6:]:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["assistant"]})

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    assistant_reply = response.choices[0].message.content

    history.append({
        "user": user_message,
        "assistant": assistant_reply
    })

    save_history(history)

    return assistant_reply
