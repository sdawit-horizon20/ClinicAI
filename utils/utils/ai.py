import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are ClinicAI, a healthcare assistant.
Provide general medical information only.
Do not diagnose or prescribe.
Always recommend seeing a doctor if symptoms are serious.
"""

def get_ai_response(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message["content"]
