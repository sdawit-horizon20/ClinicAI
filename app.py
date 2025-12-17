import gradio as gr
import openai
import os
import json

# Set your OpenAI API key in environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Database file for storing chat history (optional)
DB_FILE = "database/chat_history.json"

# Ensure database folder exists
os.makedirs("database", exist_ok=True)

# Load previous chat history if exists
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        chat_history_db = json.load(f)
else:
    chat_history_db = []

# AI response function using OpenAI GPT
def ai_response(user_message, chat_history):
    messages = [{"role": "system", "content": "You are ClinicAI, a helpful healthcare assistant. Provide accurate, safe, and empathetic medical advice."}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_message})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Change to gpt-4 if available
        messages=messages,
        max_tokens=300,
        temperature=0.7
    )
    
    return response.choices[0].message['content']

# Function to handle chat updates
def respond(message, chat_history):
    chat_history.append({"role": "user", "content": message})
    response = ai_response(message, chat_history)
    chat_history.append({"role": "assistant", "content": response})
    
    # Save to database
    chat_history_db.append({"user": message, "assistant": response})
    with open(DB_FILE, "w") as f:
        json.dump(chat_history_db, f, indent=4)
    
    return chat_history, chat_history

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## ClinicAI 🏥 — Your AI Healthcare Assistant")
    
    chatbot = gr.Chatbot(label="ClinicAI Chat")
    msg = gr.Textbox(label="Type your symptoms or questions here...")
    msg.submit(respond, [msg, chatbot], [chatbot, chatbot])

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    share=False
)
