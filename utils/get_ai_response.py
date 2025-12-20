import os
from openai import OpenAI

MODEL_NAME = "gpt-4o-mini"

def get_ai_response(user_message):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        timeout=30
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are ClinicAI, a medical assistant."},
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content
