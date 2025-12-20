import gradio as gr
from utils.ai import get_ai_response


def chat(message, history):
    if not message:
        return history, ""

    reply = get_ai_response(message)
    history.append((message, reply))
    return history, ""


with gr.Blocks(title="ClinicAI 🏥") as demo:
    gr.Markdown("## 🏥 ClinicAI – Healthcare AI Assistant")

    chatbot = gr.Chatbot(height=450)  # tuples by default in Gradio 6

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Ask a medical question...",
            scale=4
        )
        send = gr.Button("Send 🩺", scale=1)

    clear = gr.Button("Clear")

    msg.submit(chat, [msg, chatbot], [chatbot, msg])
    send.click(chat, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], None, chatbot)

demo.launch(server_name="0.0.0.0", server_port=10000)
