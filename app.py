import gradio as gr
from utils.ai import get_ai_response

def chat(user_message, history):
    reply = get_ai_response(user_message)
    history.append((user_message, reply))
    return history, ""

def clear_chat():
    return []

with gr.Blocks(title="ClinicAI") as app:
    gr.Markdown("## 🏥 ClinicAI – Medical Assistant")

    chatbot = gr.Chatbot(height=450)
    msg = gr.Textbox(placeholder="Ask a medical question...")
    
    with gr.Row():
        send = gr.Button("Send")
        clear = gr.Button("Clear Chat")

    send.click(chat, inputs=[msg, chatbot], outputs=[chatbot, msg])
    clear.click(clear_chat, outputs=chatbot)

app.launch(server_name="0.0.0.0", server_port=7860)
