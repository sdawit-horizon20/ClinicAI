import gradio as gr

def respond(user_message, history):
    if history is None:
        history = []

    if not user_message:
        return history

    history.append(
        (user_message,
         "I am ClinicAI 🤍. I provide general health information only. "
         "This is not medical advice. Please consult a healthcare professional.")
    )

    return history


with gr.Blocks() as demo:
    gr.Markdown(
        "# 🏥 ClinicAI\n"
        "_Educational use only. Not a medical diagnosis._"
    )

    chatbot = gr.Chatbot(height=500)
    msg = gr.Textbox(placeholder="Ask a health question…")
    send = gr.Button("Send")
    clear = gr.Button("Clear")

    send.click(respond, inputs=[msg, chatbot], outputs=[chatbot])
    clear.click(lambda: [], outputs=[chatbot])


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=10000)
