import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are ClinicAI, a medical assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
