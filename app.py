import gradio as gr

# --------- AI RESPONSE FUNCTION ----------
def respond(user_message, history):
    history = history or []

    # User message
    history.append({
        "role": "user",
        "content": user_message
    })

    # AI reply (replace later with real AI model)
    ai_reply = "Hello 👋 I am **ClinicAI**, your healthcare assistant 🏥"

    history.append({
        "role": "assistant",
        "content": ai_reply
    })

    return history, history, ""


# --------- UI ----------
with gr.Blocks(title="ClinicAI 🏥") as demo:
    gr.Markdown(
        """
        # 🏥 ClinicAI
        *Your AI Healthcare Assistant*
        """
    )

    chatbot = gr.Chatbot(
        type="messages",
        height=500
    )

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Type your message here...",
            show_label=False,
            scale=4
        )
        send_btn = gr.Button("Send ☕️", scale=1)

    # Submit by ENTER
    msg.submit(
        respond,
        inputs=[msg, chatbot],
        outputs=[chatbot, chatbot, msg]
    )

    # Submit by SEND button
    send_btn.click(
        respond,
        inputs=[msg, chatbot],
        outputs=[chatbot, chatbot, msg]
    )

demo.launch(server_name="0.0.0.0", server_port=10000)
