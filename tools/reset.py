import os

def reset_schedule():
    if os.path.exists("schedule_data.json"):
        os.remove("schedule_data.json")
        print("schedule_data.json cleared.")
    else:
        print("No schedule_data.json found.")

def reset_journal():
    if os.path.exists("journal_data.json"):
        os.remove("journal_data.json")
        print("journal_data.json cleared.")
    else:
        print("No journal_data.json found.")

