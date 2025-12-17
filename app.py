import gradio as gr

def respond(message, *args):
    return (
        "Hello 👨‍⚕️🤍\n\n"
        "I am ClinicAI, your healthcare assistant.\n\n"
        "I can help you understand symptoms, give general health guidance, "
        "and tell you when to seek medical care.\n\n"
        "How can I help you today?"
    )

demo = gr.ChatInterface(
    fn=respond,
    title="🏥 ClinicAI",
    description="Your AI Healthcare Assistant"
)

demo.launch(server_name="0.0.0.0", server_port=10000)
