import gradio as gr
import os

# -------------------------------
# ClinicAI core chat function
# -------------------------------
def clinicai_chat(user_message, chat_history):
    if not user_message:
        return chat_history, ""

    if chat_history is None:
        chat_history = []

    # ⚠️ Replace this with real AI logic later
    ai_response = (
        "🩺 ClinicAI: I’m here to help with health-related questions. "
        "Please note I do not replace a licensed doctor."
    )

    chat_history.append((user_message, ai_response))
    return chat_history, ""


# -------------------------------
# Gradio UI
# -------------------------------
with gr.Blocks(title="ClinicAI 🏥🤖") as demo:
    gr.Markdown(
        """
        # 🏥 ClinicAI  
        **AI-powered Healthcare Assistant**  
        _Educational use only – not a medical diagnosis._
        """
    )

    chatbot = gr.Chatbot(
        height=500,
        bubble_full_width=False
    )

    with gr.Row():
        txt = gr.Textbox(
            placeholder="Type your health question here...",
            show_label=False,
            scale=4
        )
        send_btn = gr.Button("Send", scale=1)

    # Button click
    send_btn.click(
        clinicai_chat,
        inputs=[txt, chatbot],
        outputs=[chatbot, txt]
    )

    # Enter key submit
    txt.submit(
        clinicai_chat,
        inputs=[txt, chatbot],
        outputs=[chatbot, txt]
    )

    gr.Markdown(
        "⚠️ **Disclaimer:** ClinicAI provides general health information only."
    )


# -------------------------------
# Render PORT binding
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )
