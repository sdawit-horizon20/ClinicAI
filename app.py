import gradio as gr

def respond(message, history):
    history = history or []

    history.append({
        "role": "user",
        "content": message
    })

    history.append({
        "role": "assistant",
        "content": "Hello 👋 I am ClinicAI, your healthcare assistant 🏥"
    })

    return history

demo = gr.ChatInterface(
    fn=respond,
    title="🏥 ClinicAI",
    description="Your AI Healthcare Assistant",
)

demo.launch(server_name="0.0.0.0", server_port=10000)
