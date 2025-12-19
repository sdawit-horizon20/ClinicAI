import os
import gradio as gr
from utils.ai import get_ai_response
from utils.db import save_chat

SYSTEM_PROMPT = (
    "You are ClinicAI, a professional healthcare assistant. "
    "You provide safe, general medical information, not diagnoses."
)


def chat(user_input, history):
    history = history or []

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for u, a in history:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": a})

    messages.append({"role": "user", "content": user_input})

    response = get_ai_response(messages)

    history.append((user_input, response))
    save_chat(user_input, response)

    return history, ""


with gr.Blocks(title="ClinicAI") as demo:
    gr.Markdown("## 🏥 ClinicAI – Intelligent Healthcare Assistant")

    chatbot = gr.Chatbot(height=450)
    msg = gr.Textbox(placeholder="Describe your symptoms…")
    send = gr.Button("Send 💬")

    send.click(chat, inputs=[msg, chatbot], outputs=[chatbot, msg])


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 10000)))
