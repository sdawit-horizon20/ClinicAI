import gradio as gr

-----------------------------

ClinicAI Chat Logic

-----------------------------

def respond(user_message, history): """ Chatbot expects a list of dicts: {"role": "user"|"assistant", "content": str} """ # Always ensure history is a list if history is None: history = []

# Ignore empty submits
if not user_message:
    return history

# Append user message
history.append({
    "role": "user",
    "content": str(user_message)
})

# Safe placeholder response
assistant_reply = (
    "I am ClinicAI 🤍. I provide general health information only. "
    "I am not a doctor, and this is not a medical diagnosis. "
    "Please consult a licensed healthcare professional.\n\n"
    "How can I help you today?"
)

# Append assistant message
history.append({
    "role": "assistant",
    "content": assistant_reply
})

return history

-----------------------------

Gradio UI

-----------------------------

with gr.Blocks(title="ClinicAI – Healthcare Assistant") as demo: gr.Markdown( """ # 🏥 ClinicAI AI-powered healthcare assistant
Educational use only. Not a medical diagnosis.
""" )

chatbot = gr.Chatbot(
    type="messages",
    height=500
)

msg = gr.Textbox(
    placeholder="Ask a health-related question...",
    label="Your message",
    lines=2
)

send = gr.Button("Send")
clear = gr.Button("Clear Chat")

send.click(
    respond,
    inputs=[msg, chatbot],
    outputs=[chatbot]
)

clear.click(
    lambda: [],
    outputs=[chatbot]
)

-----------------------------

App Launch (Render-safe)

-----------------------------

if name == "main": demo.launch(server_name="0.0.0.0", server_port=10000)
