import gradio as gr
from utils.ai import get_ai_response


def respond(user_message, history):
    if history is None:
        history = []

    # user message
    history.append({
        "role": "user",
        "content": user_message
    })

    # AI response
    reply = get_ai_response(user_message)

    history.append({
        "role": "assistant",
        "content": reply
    })

    return history


with gr.Blocks() as demo:
    gr.Markdown("## 🏥 ClinicAI — Your Health Assistant")

    chatbot = gr.Chatbot(height=500)

    msg = gr.Textbox(
        placeholder="Describe your symptoms...",
        show_label=False
    )

    send = gr.Button("Send")
    clear = gr.Button("Clear")

    send.click(
        respond,
        inputs=[msg, chatbot],
        outputs=chatbot
    )

    clear.click(
        lambda: [],
        outputs=chatbot
    )

demo.launch(server_name="0.0.0.0", server_port=10000)
