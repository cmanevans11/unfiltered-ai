import gradio as gr
from console_assistant import respond  # reuse your existing logic
from datetime import datetime

# --- Format output exactly like your console version ---
def format_output(role, msg):
    return (
        f"**{role} @ {datetime.now().strftime('%H:%M:%S')}**\n\n"
        f"{msg}"
    )

# --- Gradio chat wrapper ---
def chat_interface(message, history):
    reply = respond(message)

    # Append messages in a clean UI structure
    history.append(
        (format_output("Founder", message),
         format_output("Assistant", reply))
    )
    return history, history

# --- Launch Chat Interface ---
with gr.Blocks() as demo:
    gr.Markdown("# 🌐 UNFILTERED AI — Browser Assistant")

    chatbot = gr.Chatbot(
        height=600,
        render_markdown=True
    )

    msg = gr.Textbox(
        label="Type your message",
        placeholder="Speak to your assistant…"
    )

    msg.submit(chat_interface, [msg, chatbot], [chatbot, chatbot])

demo.launch()
