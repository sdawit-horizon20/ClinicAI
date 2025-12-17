import os
import openai
import gradio as gr

# -----------------------------
# 1️⃣ OpenAI API Key
# -----------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------
# 2️⃣ AI Response Function
# -----------------------------
def respond(user_message, history=None):
    history = history or []

    messages = [{"role": "system", "content": "You are ClinicAI, a helpful healthcare assistant. Give safe, general health advice and encourage seeing a doctor if needed."}]
    
    for entry in history:
        messages.append({"role": "user", "content": entry[0]})
        messages.append({"role": "assistant", "content": entry[1]})
    
    messages.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )
        ai_reply = response.choices[0].message.content.strip()
    except Exception as e:
        ai_reply = "⚠️ Sorry, I couldn't process your request at the moment."

    history.append((user_message, ai_reply))
    return history, history, ""  # clears input box

# -----------------------------
# 3️⃣ Gradio UI
# -----------------------------
with gr.Blocks(title="🏥 ClinicAI") as demo:
    gr.Markdown("# 🏥 ClinicAI\nYour AI Healthcare Assistant")

    chatbot = gr.Chatbot(height=500)

    with gr.Row():
        msg = gr.Textbox(placeholder="Type your message here...", show_label=False, scale=4)
        send_btn = gr.Button("Send ☕️", scale=1)

    # Enter key
    msg.submit(respond, [msg, chatbot], [chatbot, chatbot, msg])
    # Send button
    send_btn.click(respond, [msg, chatbot], [chatbot, chatbot, msg])

# -----------------------------
# 4️⃣ Launch
# -----------------------------
demo.launch(server_name="0.0.0.0", server_port=10000)
