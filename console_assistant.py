import os
import sys
from datetime import datetime

# === Imports from your project ===
from llm.engine import analyze_text
from core.encoder import encode_entry
from core.memory import save_entry, load_entries, save_to_long_memory
from core.conversation_memory import load_conversation_history, save_conversation_history
from core.identity import COMPASSION_CORE
from core.founder_page import FOUNDER_PAGE_TEXT
from core.dimensional_prompt import DIMENSIONAL_SCAFFOLD


# === Load conversation memory ===
conversation_history = load_conversation_history()
MAX_HISTORY = 10  # keep it small for token efficiency


# ============================================================
# Recent memory retrieval
# ============================================================

def get_recent_memories(n=3):
    entries = load_entries()
    if not entries:
        return "(no memories yet)"

    recent = entries[-n:]
    blocks = []

    for e in recent:
        latent = e.get("latent", {})
        blocks.append(
            f"[{e['timestamp']}] "
            f"Emotion: {latent.get('emotion')}, "
            f"Intention: {latent.get('intention')}, "
            f"Reflection: {latent.get('self_reflection')}"
        )

    return "\n".join(blocks)


# ============================================================
# Formatting Helpers
# ============================================================

import re

def format_code_blocks(text):
    """
    Detects ```code``` blocks and formats them for console output.
    Converts:
        ```python
        code here
        ```
    Into:
        [CODE BLOCK: python]
        code here
        [END CODE BLOCK]
    """
    pattern = r"```(\w+)?\n(.*?)```"
    
    def repl(match):
        lang = match.group(1) or "code"
        code = match.group(2)
        return (
            f"\n[BEGIN {lang.upper()} BLOCK]\n"
            f"{code}\n"
            f"[END {lang.upper()} BLOCK]\n"
        )

    return re.sub(pattern, repl, text, flags=re.DOTALL)

def format_user(msg):
    return f"\n──────── USER @ {datetime.now().strftime('%H:%M:%S')} ────────\n{msg}\n"

def format_assistant(msg):
    msg = format_code_blocks(msg)  # ← NEW LINE
    return (
        f"\n──────── ASSISTANT @ {datetime.now().strftime('%H:%M:%S')} ────────\n"
        f"{msg}\n"
    )


def format_journal(msg):
    return f"\n──── JOURNAL ENTRY @ {datetime.now().strftime('%H:%M:%S')} ────\n{msg}\n"




# ============================================================
# LLM Interaction
# ============================================================

def respond(message):
    from openai import OpenAI
    client = OpenAI()

    recent_memory_text = get_recent_memories()

    # Combine all system-level philosophy into one prompt
    system_prompt = (
        COMPASSION_CORE +
        "\n\n" +
        DIMENSIONAL_SCAFFOLD +
        "\n\nRecent user memories:\n" +
        recent_memory_text +
        "\nIf memories are empty, ignore that section."
    )

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # Short-term history
    for role, content in conversation_history:
        messages.append({"role": role, "content": content})

    # Current user message
    messages.append({"role": "user", "content": message})

    # === LLM call ===
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content

    # Save to short-term memory
    conversation_history.append(("user", message))
    conversation_history.append(("assistant", reply))
    save_conversation_history(conversation_history)

    return reply


# ============================================================
# Journal entry handling
# ============================================================

def process_journal_entry(text):
    analysis = analyze_text(text)
    encoded = encode_entry(text, analysis)
    save_entry(encoded)

    return (
        "Journal entry saved.\n"
        f"Emotion detected: {analysis.get('emotion')}\n"
        f"Goal detected: {analysis.get('goals')}"
    )


# ============================================================
# MAIN LOOP
# ============================================================

print("UNFILTERED AI — Conversational Mode\n")

while True:
    user_input = input("Founder > ").strip()

    if user_input.lower() in ["exit", "quit"]:
        print(format_assistant("Ending session."))
        break

    # Journal Mode
    if user_input.lower().startswith("journal:"):
        content = user_input[len("journal:"):].strip()
        reply = process_journal_entry(content)
        print(format_journal(reply))
        continue

    # Save founder page permanently
    if user_input.lower() == "store_founder_page":
        save_to_long_memory(FOUNDER_PAGE_TEXT)
        print(format_assistant("Founder identity saved permanently."))
        continue

    # Normal conversation
    reply = respond(user_input)
    print(format_assistant(reply))
