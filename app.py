import os
import openai
import gradio as gr

# -----------------------------
# 1️⃣ Set your OpenAI API key
# -----------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in Render secrets

# -----------------------------
# 2️⃣ AI response function
# -----------------------------
def respond(user_message, history=None):
    history = history or []

    # Build messages for OpenAI
    messages = [{"role": "system", "content": "You are ClinicAI, a helpful healthcare assistant. Give safe, general health advice and always encourage users to see a doctor if needed."}]
    
    # Add previous conversation for context
    for entry in history:
        messages.append({"role": "user", "content": entry[0]})
        messages.append({"role": "assistant", "content": entry[1]})

    # Add current user input
    messages.append({"role": "user", "content": user_message})

    # Call OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change to gpt-4 if available
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )
        ai_reply = response.choices[0].message.content.strip()
    except Exception as e:
        ai_reply = "⚠️ Sorry, I couldn't process your request. Please try again later."

    # Append to history
    history.append((user_message, ai_reply))

    return history, history, ""  # Third value clears the input box

# -----------------------------
# 3️⃣ Gradio UI
# -----------------------------
with gr.Blocks(title="🏥 ClinicAI") as demo:
    gr.Markdown(
        """
        # 🏥 ClinicAI
        Your AI Healthcare Assistant
        """
    )

    chatbot = gr.Chatbot(height=500)  # Tuple-based history

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Type your message here...",
            show_label=False,
            scale=4
        )
        send_btn = gr.Button("Send ☕️", scale=1)

    # Submit by Enter key
    msg.submit(respond, [msg, chatbot], [chatbot, chatbot, msg])

    # Submit by Send button
    send_btn.click(respond, [msg, chatbot], [chatbot, chatbot, msg])

# -----------------------------
# 4️⃣ Launch
# -----------------------------
demo.launch(server_name="0.0.0.0", server_port=10000)
