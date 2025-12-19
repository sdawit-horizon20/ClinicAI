import gradio as gr
import os

from utils.ai import get_ai_response


SYSTEM_WELCOME = (
    "Hello 👨‍⚕️🤍\n\n"
    "I am ClinicAI, your healthcare assistant.\n\n"
    "I can help you understand symptoms, give general health guidance, "
    "and tell you when to seek medical care.\n\n"
    "How can I help you today?"
)


def chat(user_input, history):
    if not user_input:
        return history, history

    ai_reply = get_ai_response(user_input)

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": ai_reply})

    return history, history


with gr.Blocks(title="ClinicAI 🏥") as demo:
    gr.Markdown("## 🏥 ClinicAI — Your Healthcare Assistant")

    chatbot = gr.Chatbot(
        value=[{"role": "assistant", "content": SYSTEM_WELCOME}],
        type="messages",
        height=450,
    )

    msg = gr.Textbox(
        placeholder="Describe your symptoms...",
        label="Patient Input",
    )

    send = gr.Button("Send 💬")

    send.click(
        chat,
        inputs=[msg, chatbot],
        outputs=[chatbot, chatbot],
    )

    msg.submit(
        chat,
        inputs=[msg, chatbot],
        outputs=[chatbot, chatbot],
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
