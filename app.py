import os
import gradio as gr
from openai import OpenAI

# =========================
# OpenAI Client
# =========================
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = (
    "You are ClinicAI, a helpful and safe healthcare assistant. "
    "You provide general medical information only and always advise "
    "users to consult a licensed healthcare professional."
)

# =========================
# AI Response Function
# =========================
def get_ai_response(user_message, history):
    if not user_message:
        return history

    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Convert chat history to OpenAI format
        for user, assistant in history:
            messages.append({"role": "user", "content": user})
            messages.append({"role": "assistant", "content": assistant})

        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.4,
            timeout=30
        )

        reply = response.choices[0].message.content
        history.append((user_message, reply))
        return history

    except Exception as e:
        history.append(
            (user_message, "⚠️ ClinicAI error: Unable to connect to AI service.")
        )
        return history


# =========================
# Clear Chat Function  ✅ FIX
# =========================
def clear_chat():
    return [], ""


# =========================
# Gradio UI
# =========================
with gr.Blocks(title="ClinicAI") as demo:
    gr.Markdown("## 🏥 ClinicAI – Healthcare Assistant")

    chatbot = gr.Chatbot(height=450)
    msg = gr.Textbox(
        placeholder="Ask a health-related question...",
        label="Your Message"
    )

    with gr.Row():
        send_btn = gr.Button("Send")
        clear_btn = gr.Button("🧹 Clear Chat")

    send_btn.click(
        fn=get_ai_response,
        inputs=[msg, chatbot],
        outputs=chatbot
    )

    msg.submit(
        fn=get_ai_response,
        inputs=[msg, chatbot],
        outputs=chatbot
    )

    clear_btn.click(
        fn=clear_chat,
        inputs=None,
        outputs=[chatbot, msg]
    )


# =========================
# Launch (Render-safe)
# =========================
demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000)),
    show_error=True
    )
