from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are ClinicAI, a helpful medical assistant."},
                {"role": "user", "content": user_message}
            ],
            timeout=30
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ ClinicAI error: {str(e)}"
