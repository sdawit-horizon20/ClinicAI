import gradio as gr
from utils.ai import get_ai_response
from utils.translator import translate_text
from utils.db import save_chat

def chat_interface(user_input, lang="en"):
    ai_reply = get_ai_response(user_input)
    translated_reply = translate_text(ai_reply, lang)
    save_chat(user_input, translated_reply)
    return translated_reply

iface = gr.Interface(
    fn=chat_interface,
    inputs=[gr.Textbox(label="Your message"), gr.Dropdown(["en","fr","es"], label="Language")],
    outputs="text",
    title="ClinicAI - Super Advanced"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=8080)
