import os
import gradio as gr

USE_OPENAI = True  # change to False to disable OpenAI completely

def clinic_ai(chat_history):
    try:
        if not chat_history:
            return chat_history

        user_message = chat_history[-1]["content"]

        reply = None

        if USE_OPENAI:
            try:
                from openai import OpenAI

                client = OpenAI(
                    api_key=os.environ.get("OPENAI_API_KEY"),
                    timeout=20
                )

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are ClinicAI, a medical assistant."},
                        {"role": "user", "content": user_message}
                    ]
                )

                reply = response.choices[0].message.content

            except Exception as e:
                print("⚠️ OpenAI unavailable:", repr(e))

        # 🔁 FALLBACK RESPONSE (ALWAYS WORKS)
        if not reply:
            reply = (
                "👩‍⚕️ **ClinicAI (Offline Mode)**\n\n"
                "I’m currently unable to reach the AI service, but I’m still here.\n\n"
                f"You said:\n> {user_message}\n\n"
                "⚠️ This is not medical advice."
            )

        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        return chat_history

    except Exception as e:
        print("❌ UNEXPECTED ERROR:", repr(e))
        return [{
            "role": "assistant",
            "content": "⚠️ System error. Please refresh the page."
        }]

with gr.Blocks(title="ClinicAI") as demo:
    gr.Markdown(
        "# 🏥 ClinicAI\n"
        "_AI-powered medical assistant_  \n"
        "⚠️ Not a substitute for professional medical advice."
    )

    chatbot = gr.Chatbot(type="messages", height=450)
    msg = gr.Textbox(placeholder="Describe your symptoms...")

    msg.submit(fn=clinic_ai, inputs=chatbot, outputs=chatbot)

demo.launch(server_name="0.0.0.0", server_port=10000)
