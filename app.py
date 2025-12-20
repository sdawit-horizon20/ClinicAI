import gradio as gr

def clinic_ai(chat_history):
    try:
        user_message = chat_history[-1]["content"]

        reply = f"👩‍⚕️ ClinicAI response: You said '{user_message}'"

        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        return chat_history

    except Exception as e:
        return [{
            "role": "assistant",
            "content": f"⚠️ ClinicAI internal error: {str(e)}"
        }]

with gr.Blocks() as demo:
    gr.Markdown("## 🏥 ClinicAI")

    chatbot = gr.Chatbot(type="messages", height=450)

    msg = gr.Textbox(placeholder="Describe your symptoms...")
    clear = gr.Button("Clear")

    msg.submit(
        fn=clinic_ai,
        inputs=chatbot,
        outputs=chatbot
    )

    clear.click(lambda: [], None, chatbot)

demo.launch(server_name="0.0.0.0", server_port=10000)
