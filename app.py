import gradio as gr
from utils.ai import get_ai_response

def respond(user_message, history):
    if history is None:
        history = []

    # add user message
    history.append({
        "role": "user",
        "content": user_message
    })

    # get AI reply
    ai_reply = get_ai_response(user_message)

    # add assistant message
    history.append({
        "role": "assistant",
        "content": ai_reply
    })

    return history, history


with gr.Blocks() as demo:
    gr.Markdown("## 🏥 ClinicAI — Your Health Assistant")

    chatbot = gr.Chatbot(type="messages", height=500)

    msg = gr.Textbox(
        placeholder="Describe your symptoms...",
        show_label=False
    )

    send = gr.Button("Send")
    clear = gr.Button("Clear")

    send.click(
        respond,
        inputs=[msg, chatbot],
        outputs=[chatbot, chatbot]
    )

    clear.click(
        lambda: [],
        outputs=chatbot
    )

demo.launch(server_name="0.0.0.0", server_port=10000)
