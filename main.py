import sys
import os
print("CWD:", os.getcwd())

from llm.engine import analyze_text
from core.encoder import encode_entry
from core.memory import save_entry, load_entries
from core.decoder import decoder_behaviors
from core.patterns import (
    detect_grounding_needed,
    detect_habit_frequency,
    detect_time_pattern,
    habit_streak,
    predict_next_habit_time
)

# FIRST INPUT — before anything else
text = input("\nType a journal entry to process:\n> ")

# RESET COMMAND
if text.strip().lower() == "reset":
    from tools.reset import reset_schedule, reset_journal
    reset_schedule()
    reset_journal()
    sys.exit()


def process_entry(text):
    print("\n=== RAW INPUT ===")
    print(text)

    analysis = analyze_text(text)

    print("\n=== LLM ANALYSIS ===")
    print(analysis)

    encoded = encode_entry(text, analysis)

    print("\n=== ENCODED ENTRY ===")
    print(encoded)

    save_entry(encoded)

    suggestions = decoder_behaviors(encoded)

    print("\n=== ASSISTANT SUGGESTIONS ===")
    for s in suggestions:
        print(" -", s)

    return encoded


def test_prediction():
    entries = load_entries()
    predicted_hour = predict_next_habit_time(entries, "tiktok")

    print("\n=== PATTERN PREDICTION ===")
    print("Predicted TikTok hour:", predicted_hour)

    # simulate current hour = predicted hour
    current_hour = predicted_hour

    print("Current hour:", current_hour)

    if predicted_hour is not None and current_hour == predicted_hour:
        print("\n🔔 Notification fired: TikTok again? Interesting 😏")
    else:
        print("\nNo notification triggered.")


if __name__ == "__main__":
    print("===================================")
    print("        UNFILTERED (CONSOLE) AI")
    print("===================================")

    process_entry(text)
    test_prediction()