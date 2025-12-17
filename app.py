import os
import gradio as gr
from openai import OpenAI

# -----------------------------
# OpenAI Client
# -----------------------------
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=30
)

# -----------------------------
# AI Response Function
# -----------------------------
def clinicai_response(message, history):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=message
        )
        return response.output_text

    except Exception as e:
        return f"⚠️ ClinicAI error: {str(e)}"


# -----------------------------
# Gradio UI
# -----------------------------
with gr.Blocks(title="ClinicAI") as demo:
    gr.Markdown("## 🏥 ClinicAI – Healthcare Assistant")
    gr.Markdown("Ask health-related questions. This is not a replacement for a doctor.")

    chatbot = gr.Chatbot(height=450)
    msg = gr.Textbox(
        placeholder="Type your health question here...",
        label="Your Message"
    )
    clear = gr.Button("Clear Chat")

    def respond(user_message, chat_history):
        bot_message = clinicai_response(user_message, chat_history)
        chat_history.append((user_message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: [], None, chatbot)

# -----------------------------
# Run App (Render compatible)
# -----------------------------
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 10000)),
        show_error=True
    )
