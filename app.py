import os
import gradio as gr
from openai import OpenAI

# Initialize OpenAI client (API key comes from Render environment)
client = OpenAI()

def ai_response(user_message, chat_history):
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are ClinicAI, a helpful healthcare assistant. "
                    "Provide safe, empathetic medical information. "
                    "Do not diagnose. Encourage consulting professionals when needed."
                )
            }
        ]

        messages.extend(chat_history)
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        # This will show the REAL error in the chatbot
        return f"⚠️ ClinicAI error: {str(e)}"

def respond(message, chat_history):
    chat_history.append({"role": "user", "content": message})
    reply = ai_response(message, chat_history)
    chat_history.append({"role": "assistant", "content": reply})
    return chat_history, chat_history

with gr.Blocks() as demo:
    gr.Markdown("## 🏥 ClinicAI — Healthcare Assistant")

    chatbot = gr.Chatbot(height=500)
    msg = gr.Textbox(placeholder="Describe your symptoms or ask a health question...")

    msg.submit(respond, [msg, chatbot], [chatbot, chatbot])

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    share=False
)
