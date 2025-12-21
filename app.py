import os
from dotenv import load_dotenv
import gradio as gr
import openai

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment variables!")

openai.api_key = OPENAI_API_KEY

# Main AI function
def ask_ai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Gradio interface
iface = gr.Interface(
    fn=ask_ai,
    inputs="text",
    outputs="text",
    title="ClinicAI",
    description="Ask any medical-related questions!"
)

# Launch
iface.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
