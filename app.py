import gradio as gr
import os
from openai import OpenAI, RateLimitError

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --------------------------------
# AI response handler
# --------------------------------
def clinicai_response(user_input, history):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are ClinicAI, a healthcare assistant. Do not give diagnoses."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content

    except RateLimitError:
        return (
            "⚠️ ClinicAI Notice:\n\n"
            "AI service quota has been exceeded.\n"
            "Please try again later or contact the administrator."
        )

    except Exception as e:
        return f"⚠️ ClinicAI Error: {str(e)}"


# --------------------------------
# Chat handler
# --------------------------------
def chat_handler(user_input, history):
    if history is None:
        history = []

    ai_reply = clinicai_response(user_input, history)
    history.append((user_input, ai_reply))
    return history, ""


# --------------------------------
# UI
# --------------------------------
with gr.Blocks(title="ClinicAI 🏥🤖") as demo:
    gr.Markdown(
        """
        # 🏥 ClinicAI  
        **AI-powered Healthcare Assistant**  
        _Educational use only. Not a medical diagnosis._
        """
    )

    chatbot = gr.Chatbot(height=500)

    with gr.Row():
        txt = gr.Textbox(
            placeholder="Type your health question...",
            show_label=False,
            scale=4
        )
        send = gr.Button("Send")

    send.click(chat_handler, inputs=[txt, chatbot], outputs=[chatbot, txt])
    txt.submit(chat_handler, inputs=[txt, chatbot], outputs=[chatbot, txt])

    gr.Markdown("⚠️ ClinicAI does not replace a licensed medical professional.")


# --------------------------------
# Render port binding
# --------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port)
