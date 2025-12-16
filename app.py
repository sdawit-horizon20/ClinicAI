import gradio as gr

-----------------------------

ClinicAI Chat Logic

-----------------------------

def respond(user_message, history): """ Gradio Chatbot with type='messages' expects: history = [ {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."} ] """ if history is None: history = []

# Add user message
history.append({
    "role": "user",
    "content": user_message
})

# 🔒 Placeholder medical-safe response (NO diagnosis)
assistant_reply = (
    "I am ClinicAI 🤍. I can provide general health information, "
    "but I am not a doctor. Please consult a licensed healthcare "
    "professional for diagnosis or treatment.\n\n"
    "How can I assist you today?"
)

# Add assistant message
history.append({
    "role": "assistant",
    "content": assistant_reply
})

return history

-----------------------------

Gradio UI

-----------------------------

with gr.Blocks(title="ClinicAI – Healthcare Assistant") as demo: gr.Markdown( """ # 🏥 ClinicAI Your AI-powered healthcare assistant
For educational purposes only. Not a medical diagnosis.
""" )

chatbot = gr.Chatbot(
    type="messages",
    height=500
)

msg = gr.Textbox(
    placeholder="Ask a health-related question...",
    label="Your message"
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

App Launch

-----------------------------

if name == "main": demo.launch(server_name="0.0.0.0", server_port=10000)
