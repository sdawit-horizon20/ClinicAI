import os
import openai
from utils.translator import translate_to_english, translate_from_english
from utils.db import load_history, save_history

openai.api_key = os.getenv("OPENAI_API_KEY")

def respond(user_message, history=None, user_lang='en'):
    full_history = load_history()
    history = history or []

    user_message_en = translate_to_english(user_message) if user_lang != 'en' else user_message

    messages = [{"role": "system", "content": "You are ClinicAI, a helpful healthcare assistant. Give safe, general health advice and encourage users to see a doctor if needed."}]
    for entry in full_history:
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
    full_history.append((user_message, ai_reply_translated))

    save_history(full_history)

    return history, history, ""  # clears input box
