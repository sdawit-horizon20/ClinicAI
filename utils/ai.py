import os
from openai import OpenAI

# Initialize OpenAI client (new SDK)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_ai_response(user_message: str) -> str:
    """
    Sends user input to OpenAI and returns the response text.
    """

    if not client.api_key:
        return "⚠️ OpenAI API key is not configured."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful healthcare AI assistant."},
                {"role": "user", "content": user_message},
            ],
            temperature=0.4,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"
