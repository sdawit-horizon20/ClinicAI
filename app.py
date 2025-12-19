import gradio as gr
from utils.ai import get_ai_response


def chat(user_input, history):
    response = get_ai_response(user_input)
    history.append((user_input, response))
    return history, ""


with gr.Blocks(title="ClinicAI 🏥") as demo:
    gr.Markdown("## 🏥 ClinicAI – Healthcare AI Assistant")

    chatbot = gr.Chatbot(height=450)
    msg = gr.Textbox(
        placeholder="Ask a medical question...",
        show_label=False
    )
    clear = gr.Button("Clear Chat")

    msg.submit(chat, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], None, chatbot)

demo.launch(server_name="0.0.0.0", server_port=10000)
