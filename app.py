import gradio as gr

def respond(message, *args):
    msg = message.lower()

    # Greeting
    if any(word in msg for word in ["hello", "hi", "greetings", "doctor"]):
        return (
            "Hello 👨‍⚕️🤍\n\n"
            "I am ClinicAI, your healthcare assistant.\n\n"
            "How can I help you today?"
        )

    # Fever + cough
    if "fever" in msg and "cough" in msg:
        return (
            "I’m sorry you’re feeling unwell 🤍\n\n"
            "Fever and cough together are commonly caused by infections such as flu, COVID-19, or other respiratory infections.\n\n"
            "💡 What you can do now:\n"
            "- Rest and drink plenty of fluids\n"
            "- Monitor your temperature\n"
            "- Use paracetamol if advised by a healthcare professional\n\n"
            "⚠️ Please seek medical care urgently if you have:\n"
            "- Difficulty breathing\n"
            "- Chest pain\n"
            "- Fever lasting more than 3 days\n\n"
            "Would you like me to ask a few questions to better understand your symptoms?"
        )

    # Default response
    return (
        "Thank you for sharing 🤍\n\n"
        "Could you please tell me more about your symptoms?\n"
        "For example: fever, pain, cough, headache, or stomach problems."
    )

demo = gr.ChatInterface(
    fn=respond,
    title="🏥 ClinicAI",
    description="Your AI Healthcare Assistant"
)

demo.launch(server_name="0.0.0.0", server_port=10000)
