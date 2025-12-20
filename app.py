import gradio as gr

# =========================
# ClinicAI core logic
# =========================
def clinic_ai(chat_history):
    try:
        # Safety: if empty history, do nothing
        if not chat_history:
            return chat_history

        # Get last user message
        user_message = chat_history[-1]["content"]

        # ---- YOUR AI LOGIC GOES HERE ----
        # (for now, simple demo response)
        ai_reply = (
            "👩‍⚕️ **ClinicAI**\n\n"
            f"I received your message:\n> {user_message}\n\n"
            "⚠️ This is not medical advice."
        )

        # Append assistant response
        chat_history.append({
            "role": "assistant",
            "content": ai_reply
        })

        return chat_history

    except Exception as e:
        # Log real error to Render logs
        print("❌ ClinicAI INTERNAL ERROR:", repr(e))

        # Show safe message to user
        return [{
            "role": "assistant",
            "content": "⚠️ ClinicAI encountered an internal error. Please try again."
        }]


# =========================
# Gradio UI
# =========================
with gr.Blocks(title="ClinicAI") as demo:
    gr.Markdown(
        """
        # 🏥 ClinicAI  
        _AI-powered healthcare assistant_  
        ⚠️ Not a substitute for professional medical advice.
        """
    )

    chatbot = gr.Chatbot(
        type="messages",
        height=450
    )

    msg = gr.Textbox(
        placeholder="Describe your symptoms...",
        show_label=False
    )

    clear = gr.Button("🧹 Clear Chat")

    # Submit message
    msg.submit(
        fn=clinic_ai,
        inputs=chatbot,
        outputs=chatbot
    )

    # Clear chat
    clear.click(
        lambda: [],
        None,
        chatbot
    )


# =========================
# Launch (Render compatible)
# =========================
demo.launch(
    server_name="0.0.0.0",
    server_port=10000
    )
