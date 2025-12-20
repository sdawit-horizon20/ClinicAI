import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(prompt: str) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return "❌ OPENAI_API_KEY is missing on the server."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are ClinicAI, a helpful medical assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        # This will appear in Render logs
        print("AI ERROR:", e)
        return f"⚠️ AI error: {str(e)}"
