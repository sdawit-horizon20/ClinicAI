import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def get_ai_response(prompt: str) -> str:
    """Call OpenAI API to get AI response"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content.strip()
