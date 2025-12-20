import os
import gradio as gr
from openai import OpenAI

def clinic_ai(chat_history):
    try:
        if not chat_history:
            return chat_history

        user_message = chat_history[-1]["content"]

        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            timeout=30
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are ClinicAI, a medical assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content

        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        return chat_history

    except Exception as e:
        print("❌ ClinicAI ERROR:", repr(e))
        return [{
            "role": "assistant",
            "content": "⚠️ AI service temporarily unavailable. Please try again."
        }]

with gr.Blocks(title="ClinicAI") as demo:
    gr.Markdown("# 🏥 ClinicAI")

    chatbot = gr.Chatbot(type="messages", height=450)
    msg = gr.Textbox(placeholder="Describe your symptoms...")

    msg.submit(fn=clinic_ai, inputs=chatbot, outputs=chatbot)

demo.launch(server_name="0.0.0.0", server_port=10000)
