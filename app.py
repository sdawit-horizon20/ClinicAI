import gradio as gr
from utils.ai import get_ai_response


def chat(user_input, history):
    if not user_input.strip():
        return history, ""

    response = get_ai_response(user_input)
    history.append((user_input, response))
    return history, ""


with gr.Blocks(title="ClinicAI 🏥") as demo:
    gr.Markdown("## 🏥 ClinicAI – Healthcare AI Assistant")

    chatbot = gr.Chatbot(
        height=450,
        type="tuples"   # ⭐ CRITICAL FIX
    )

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Type your medical question here...",
            show_label=False,
            scale=4
        )
        send = gr.Button("Send 🩺", scale=1)

    clear = gr.Button("Clear Chat")

    msg.submit(chat, [msg, chatbot], [chatbot, msg])
    send.click(chat, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], None, chatbot)

demo.launch(server_name="0.0.0.0", server_port=10000)
