import os
import gradio as gr
from openai import OpenAI

# =========================
# ClinicAI backend function
# =========================
def clinic_ai(chat_history):
    """
    Handles user messages, calls OpenAI, and returns updated chat history.
    """
    try:
        # Safety: do nothing if history is empty
        if not chat_history:
            return chat_history

        # Last user message
        user_message = chat_history[-1]["content"]

        # OpenAI client with API key from environment
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), timeout=30)

        # Call OpenAI ChatCompletion
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # ✅ Correct model name
            messages=[
                {"role": "system", "content": "You are ClinicAI, a friendly medical assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract AI reply
        reply = response.choices[0].message.content

        # Append assistant response to chat history
        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        return chat_history

    except Exception as e:
        # Log real error in Render logs
        print("❌ ClinicAI ERROR:", repr(e))
        # Return safe message to user
        return [{
            "role": "assistant",
            "content": "⚠️ AI service temporarily unavailable. Please try again."
        }]


# =========================
# Gradio UI
# =========================
with gr.Blocks(title="ClinicAI") as demo:
    gr.Markdown(
        """
        # 🏥 ClinicAI
        _AI-powered medical assistant_  
        ⚠️ Not a substitute for professional medical advice.
        """
    )

    # Chatbot UI
    chatbot = gr.Chatbot(type="messages", height=450)

    # Textbox for user input
    msg = gr.Textbox(
        placeholder="Describe your symptoms...",
        show_label=False
    )

    # Clear button
    clear = gr.Button("🧹 Clear Chat")

    # Submit message
    msg.submit(fn=clinic_ai, inputs=chatbot, outputs=chatbot)

    # Clear chat
    clear.click(lambda: [], None, chatbot)


# =========================
# Launch server (Render-compatible)
# =========================
demo.launch(
    server_name="0.0.0.0",
    server_port=10000
    )
