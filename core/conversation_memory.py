import json
import os

MEMORY_PATH = "conversation_history.json"
MAX_TURNS = 8  # last 8 exchanges (user+assistant = 1 turn)

def load_conversation_history():
    if not os.path.exists(MEMORY_PATH):
        return []
    try:
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def save_conversation_history(history):
    # keep only the last MAX_TURNS turns
    trimmed = history[-MAX_TURNS:]
    with open(MEMORY_PATH, "w") as f:
        json.dump(trimmed, f, indent=2)

