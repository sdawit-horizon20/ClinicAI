import gradio as gr
from utils.ai import get_ai_response


def chat(message, history):
    reply = get_ai_response(message)
    history.append((message, reply))
    return history, ""


with gr.Blocks(title="ClinicAI") as demo:
    gr.Markdown("## 🏥 ClinicAI")
    gr.Markdown("AI-powered healthcare assistant")

    chatbot = gr.Chatbot(height=450)
    msg = gr.Textbox(
        placeholder="Ask a medical question...",
        show_label=False
    )
    clear = gr.Button("Clear")

    msg.submit(chat, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], None, chatbot)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
