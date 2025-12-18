import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gradio as gr
from utils.ai import get_ai_response
from utils.db import save_chat

def chat_fn(message, history):
    if history is None:
        history = []

    history.append({"role": "user", "content": message})
    save_chat("user", message)

    try:
        reply = get_ai_response(message)
    except Exception as e:
        reply = f"⚠️ ClinicAI error: {str(e)}"

    history.append({"role": "assistant", "content": reply})
    save_chat("assistant", reply)

    return history, history

with gr.Blocks(title="ClinicAI 🏥") as demo:
    gr.Markdown("## 🏥 ClinicAI – Your Healthcare Assistant")

    chatbot = gr.Chatbot(height=500)
    state = gr.State([])

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Describe your symptoms...",
            show_label=False
        )
        send = gr.Button("Send 🩺")

    send.click(chat_fn, inputs=[msg, state], outputs=[chatbot, state])
    msg.submit(chat_fn, inputs=[msg, state], outputs=[chatbot, state])

demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 10000)))
