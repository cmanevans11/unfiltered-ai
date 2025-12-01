import os
import json
from datetime import datetime

JOURNAL_PATH = "journal_data.json"
CONVO_PATH = "conversation_history.json"


# ============================================================
#  BASIC JOURNAL ENTRY LOAD/SAVE
# ============================================================

def load_entries(path=JOURNAL_PATH):
    """Load all journal entries from disk."""
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def save_entry(entry, path=JOURNAL_PATH, importance=1):
    """
    Save a journal entry with a given importance score.

    importance meanings:
        1 = normal entry
        5 = extremely important (never trimmed)
    """
    entry["importance"] = importance

    entries = load_entries(path)
    entries.append(entry)

    with open(path, "w") as f:
        json.dump(entries, f, indent=4)


# ============================================================
#  PERMANENT FOUNDER MEMORY
# ============================================================

def save_founder_memory(text):
    """
    Save a permanent memory that represents identity, goals, or
    extremely important personal information.
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "raw": text,
        "latent": {"type": "identity"},
        "importance": 5
    }

    save_entry(entry, importance=5)

def save_to_long_memory(text):
    """
    Backwards-compatible alias for saving permanent memory.
    Allows other modules to call save_to_long_memory even if
    the main permanent memory function is save_founder_memory().
    """
    save_founder_memory(text)
    
    
# ============================================================
#  WEIGHTED MEMORY RETRIEVAL
# ============================================================

def get_recent_memories(limit=8):
    """
    Returns a weighted set of memory text for the AI system prompt.

    Strategy:
        - Include ALL permanent memories (importance ≥ 4)
        - Then include the last `limit` normal memories

    This lets the AI remember:
        - who the Founder is
        - long-term goals
        - important emotional truths
    without overwhelming the prompt.
    """

    entries = load_entries()

    if not entries:
        return ""

    # Permanent identity/guiding memories
    permanent = [e for e in entries if e.get("importance", 1) >= 4]

    # Recent “working” memories
    recent = [e for e in entries if e.get("importance", 1) < 4]
    recent = recent[-limit:]

    combined = permanent + recent

    # Format memories into readable bullet points
    memory_text = ""
    for e in combined:
        mem = e.get("raw", "")
        imp = e.get("importance", 1)
        memory_text += f"- {mem}  (importance={imp})\n"

    return memory_text


# ============================================================
#  CONVERSATION HISTORY (SHORT-TERM MEMORY)
# ============================================================

def load_conversation_history():
    """Load short-term conversation memory."""
    if not os.path.exists(CONVO_PATH):
        return []
    with open(CONVO_PATH, "r") as f:
        return json.load(f)


def save_conversation_history(history):
    """Save short-term conversation memory."""
    with open(CONVO_PATH, "w") as f:
        json.dump(history, f, indent=4)
        


