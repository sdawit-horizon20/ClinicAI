import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_response(user_message: str) -> str:
    if not openai.api_key:
        return "❌ OPENAI_API_KEY is missing."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ClinicAI, a medical assistant."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return f"❌ ClinicAI backend error: {str(e)}"
