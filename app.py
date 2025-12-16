import gradio as gr
import json
import os
import uuid
from datetime import datetime
from openai import OpenAI
from pydub import AudioSegment

# =========================
# CONFIG
# =========================
DB_PATH = "db/database.json"

MEDICAL_DISCLAIMER = (
    "⚠️ **Medical Disclaimer:**\n"
    "ClinicAI provides general healthcare information only.\n"
    "It does NOT diagnose or prescribe treatment.\n"
    "Always consult a licensed healthcare professional."
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompts for English & Amharic
SYSTEM_PROMPTS = {
    "en": """
You are ClinicAI, a Healthcare AI assistant.
You provide general medical information only.
You do NOT diagnose or prescribe treatment.
You must be empathetic, clear, and safe.
Always encourage seeing a healthcare professional.
""",
    "am": """
እንኳን ወደ ClinicAI እንኳን ደህና መጡ።
እርስዎ ሕክምና መረጃ ብቻ ይቀበላሉ።
መልሶች ሕክምና አይደሉም።
አስፈላጊ ሲሆን ወደ ባለሙያ ሐኪም መሄድን አበረታት።
"""
}

# =========================
# DATABASE HELPERS
# =========================
def load_db():
    if not os.path.exists(DB_PATH):
        return {
            "users": {},
            "sessions": {},
            "messages": {},
            "subscriptions": {},
            "uploads": {},
            "analytics": {}
        }
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)

# =========================
# USERS & SESSIONS
# =========================
def create_user():
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    db = load_db()
    db["users"][user_id] = {
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
        "subscription": "free",
        "language": "en"
    }
    save_db(db)
    return user_id

def create_session(user_id):
    session_id = f"session_{uuid.uuid4().hex[:8]}"
    db = load_db()
    db["sessions"][session_id] = {
        "session_id": session_id,
        "user_id": user_id,
        "started_at": datetime.utcnow().isoformat(),
        "ended_at": None,
        "topic": "clinic_chat"
    }
    save_db(db)
    return session_id

# =========================
# SYMPTOM CHECKER
# =========================
def symptom_checker(symptoms: str):
    symptoms = symptoms.lower()
    urgent_symptoms = [
        "chest pain", "difficulty breathing", "can't breathe",
        "severe bleeding", "unconscious", "seizure", "stroke",
        "sudden weakness"
    ]
    moderate_symptoms = [
        "fever", "persistent cough", "vomiting", "diarrhea",
        "severe headache", "abdominal pain"
    ]
    for s in urgent_symptoms:
        if s in symptoms:
            return {"risk": "🔴 Urgent", "message": "Seek immediate medical attention!"}
    for s in moderate_symptoms:
        if s in symptoms:
            return {"risk": "🟡 Medium", "message": "See a healthcare professional soon."}
    return {"risk": "🟢 Low", "message": "Mild symptoms; monitor your condition."}

# =========================
# LANGUAGE DETECTION
# =========================
def detect_language(text: str):
    amharic_chars = any("\u1200" <= ch <= "\u137F" for ch in text)
    return "am" if amharic_chars else "en"

# =========================
# AI RESPONSE
# =========================
def clinicai_response(user_message, chat_history):
    lang = detect_language(user_message)
    check = symptom_checker(user_message)
    if check["risk"] == "🔴 Urgent":
        return f"🚨 **Urgent Alert**\n{check['message']}" if lang=="en" else f"🚨 **አስቸኳይ ማስጠንቀቂያ**\n{check['message']}"

    messages = [{"role": "system", "content": SYSTEM_PROMPTS[lang]}]
    messages.extend(chat_history[-6:])
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )

    disclaimer = "⚠️ This is not a medical diagnosis." if lang=="en" else "⚠️ ይህ መልስ የሕክምና መርመራ አይደለም።"
    return f"**Risk Level:** {check['risk']}\n\n{response.choices[0].message.content}\n\n{disclaimer}"

# =========================
# SUBSCRIPTION / LIMITS
# =========================
MAX_FREE_MESSAGES = 10

def get_user_subscription(user_id):
    db = load_db()
    for sub in db["subscriptions"].values():
        if sub["user_id"]==user_id and sub["status"]=="active":
            return sub["plan"]
    return "free"

def count_user_messages_today(user_id):
    db = load_db()
    today = datetime.utcnow().date().isoformat()
    count = 0
    for msg in db["messages"].values():
        if msg["role"]=="user":
            session = db["sessions"].get(msg["session_id"])
            if session and session["user_id"]==user_id:
                if msg["timestamp"].startswith(today):
                    count +=1
    return count

# =========================
# CHAT HANDLER
# =========================
def chat_handler(user_input, history, user_id, session_id):
    db = load_db()
    plan = get_user_subscription(user_id)
    if plan=="free":
        used = count_user_messages_today(user_id)
        if used >= MAX_FREE_MESSAGES:
            warning = "💡 **Free Plan Limit Reached**. Upgrade to Premium."
            history.append({"role":"assistant","content":warning})
            return history, history

    msg_user_id = f"msg_{uuid.uuid4().hex[:8]}"
    msg_ai_id = f"msg_{uuid.uuid4().hex[:8]}"

    db["messages"][msg_user_id] = {
        "message_id": msg_user_id,
        "session_id": session_id,
        "role": "user",
        "content": user_input,
        "timestamp": datetime.utcnow().isoformat()
    }

    ai_response = clinicai_response(user_input, history)

    db["messages"][msg_ai_id] = {
        "message_id": msg_ai_id,
        "session_id": session_id,
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.utcnow().isoformat()
    }

    save_db(db)
    history.append({"role":"user","content":user_input})
    history.append({"role":"assistant","content":ai_response})

    return history, history

# =========================
# VOICE SUPPORT
# =========================
def speech_to_text(audio_file):
    if audio_file is None: return ""
    with open(audio_file,"rb") as audio:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio)
    return transcript.text

def text_to_speech(text):
    speech_file = "response.mp3"
    with client.audio.speech.with_streaming_response.create(model="gpt-4o-mini-tts", voice="alloy", input=text) as response:
        response.stream_to_file(speech_file)
    return speech_file

def voice_chat_handler(audio, history, user_id, session_id):
    user_text = speech_to_text(audio)
    if not user_text: return history, history, None
    history, _ = chat_handler(user_text, history, user_id, session_id)
    ai_reply = history[-1]["content"]
    voice_output = text_to_speech(ai_reply)
    return history, history, voice_output

# =========================
# INITIALIZE USER
# =========================
USER_ID = create_user()
SESSION_ID = create_session(USER_ID)

# =========================
# GRADIO UI
# =========================
with gr.Blocks(title="ClinicAI") as demo:
    gr.Markdown("# 🏥 ClinicAI")
    gr.Markdown("AI-powered healthcare assistant for safe medical guidance.")
    gr.Markdown(MEDICAL_DISCLAIMER)

    # FIX: Removed 'type="messages"' for new Gradio versions
    chatbot = gr.Chatbot(height=500)
    state = gr.State([])

    with gr.Tab("💬 Text Chat"):
        msg = gr.Textbox(placeholder="Describe your symptoms or ask a health question...")
        msg.submit(chat_handler, inputs=[msg,state,gr.State(USER_ID),gr.State(SESSION_ID)],
                   outputs=[chatbot,state])

    with gr.Tab("🎙️ Voice Chat"):
        audio_input = gr.Audio(type="filepath", label="Speak now")
        audio_output = gr.Audio(label="AI Response")
        audio_input.change(voice_chat_handler,
                           inputs=[audio_input,state,gr.State(USER_ID),gr.State(SESSION_ID)],
                           outputs=[chatbot,state,audio_output])

if __name__=="__main__":
    # FIX: Dynamic port for Render
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
