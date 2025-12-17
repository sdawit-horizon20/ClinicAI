import gradio as gr

def respond(message, history):
    history = history or []

    bot_reply = "Hello 👋 I am ClinicAI 🏥"

    # MUST be tuple
    history.append((message, bot_reply))

    return history, history, ""

with gr.Blocks() as demo:
    gr.Markdown("# 🏥 ClinicAI")

    chatbot = gr.Chatbot(height=500)  # ❌ NO type parameter

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Type your message…",
            show_label=False,
            scale=4
        )
        send = gr.Button("Send ☕️", scale=1)

    msg.submit(respond, [msg, chatbot], [chatbot, chatbot, msg])
    send.click(respond, [msg, chatbot], [chatbot, chatbot, msg])

demo.launch(server_name="0.0.0.0", server_port=10000)
