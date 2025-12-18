import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import gradio as gr
from utils.ai import get_ai_response
from utils.db import load_history, save_history
from utils.translator import translate_text

# Quick symptom buttons
symptoms = ["Fever 🤒", "Cough 🤧", "Headache 🤕", "Stomach Pain 🤢", "Fatigue 🥱"]

def add_symptom(symptom, chatbot):
    symptom_text = symptom.split()[0]
    return respond(symptom_text, chatbot)

# -----------------------------
# Gradio UI
# -----------------------------
with gr.Blocks(title="🏥 ClinicAI") as demo:
    gr.Markdown("# 🏥 ClinicAI\nYour AI Healthcare Assistant (Multi-lingual)")

    chatbot = gr.Chatbot(height=500)

    with gr.Row():
        msg = gr.Textbox(placeholder="Type your message here...", show_label=False, scale=4)
        send_btn = gr.Button("Send ☕️", scale=1)

    with gr.Row():
        for sym in symptoms:
            gr.Button(sym, scale=1).click(add_symptom, [gr.Button, chatbot], [chatbot, chatbot, msg])

    # Enter key
    msg.submit(respond, [msg, chatbot], [chatbot, chatbot, msg])
    # Send button
    send_btn.click(respond, [msg, chatbot], [chatbot, chatbot, msg])

demo.launch(server_name="0.0.0.0", server_port=10000)
