import os
import json
import openai
import gradio as gr
from googletrans import Translator

# -----------------------------
# 1️⃣ OpenAI API Key
# -----------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------
# 2️⃣ Translator setup
# -----------------------------
translator = Translator()

def translate_to_english(text):
    try:
        return translator.translate(text, dest='en').text
    except:
        return text

def translate_from_english(text, target_lang='en'):
    if target_lang == 'en':
        return text
    try:
        return translator.translate(text, dest=target_lang).text
    except:
        return text

# -----------------------------
# 3️⃣ AI Response Function
# -----------------------------
def respond(user_message, history=None, user_lang='en'):
    history = history or []

    user_message_en = translate_to_english(user_message) if user_lang != 'en' else user_message

    messages = [{"role": "system", "content": "You are ClinicAI, a helpful healthcare assistant. Give safe, general health advice and encourage users to see a doctor if needed."}]
    
    for entry in history:
        messages.append({"role": "user", "content": translate_to_english(entry[0])})
        messages.append({"role": "assistant", "content": entry[1]})
    
    messages.append({"role": "user", "content": user_message_en})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )
        ai_reply = response.choices[0].message.content.strip()
    except:
        ai_reply = "⚠️ Sorry, I couldn't process your request."

    ai_reply_translated = translate_from_english(ai_reply, target_lang=user_lang)

    history.append((user_message, ai_reply_translated))

    # Save history to JSON
    try:
        with open("chat_history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except:
        pass

    return history, history, ""  # clears input box

# -----------------------------
# 4️⃣ Symptom buttons
# -----------------------------
symptoms = ["Fever 🤒", "Cough 🤧", "Headache 🤕", "Stomach Pain 🤢", "Fatigue 🥱"]

def add_symptom(symptom, chatbot):
    symptom_text = symptom.split()[0]
    return respond(symptom_text, chatbot)

# -----------------------------
# 5️⃣ Gradio UI
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

# -----------------------------
# 6️⃣ Launch
# -----------------------------
demo.launch(server_name="0.0.0.0", server_port=10000)
