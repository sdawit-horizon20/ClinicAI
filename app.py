import gradio as gr

def respond(message):
    return (
        "I’m sorry you’re feeling unwell 🤍\n\n"
        "Fever and cough are common symptoms.\n\n"
        "Please rest, drink fluids, and monitor your temperature.\n"
        "If symptoms worsen or last several days, seek medical care 🏥"
    )

demo = gr.ChatInterface(
    fn=respond,
    title="🏥 ClinicAI",
    description="Your AI Healthcare Assistant"
)

demo.launch(server_name="0.0.0.0", server_port=10000)
