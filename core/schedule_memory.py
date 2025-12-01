
# core/schedule_memory.py

import json
import os
from datetime import datetime

def _get_path():
    return "schedule_data.json"


def load_schedule():
    path = _get_path()

    if not os.path.exists(path):
        return {}

    with open(path, "r") as f:
        return json.load(f)


def save_schedule(data):
    path = _get_path()

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def log_planned_task(date, task, start, end):
    data = load_schedule()

    if date not in data:
        data[date] = {"planned": [], "actual": []}

    data[date]["planned"].append({
        "task": task,
        "start": start,
        "end": end
    })

    save_schedule(data)


def log_actual_task(task):
    now = datetime.now()
    date = now.date().isoformat()
    time = now.time().strftime("%H:%M")

    data = load_schedule()

    if date not in data:
        data[date] = {"planned": [], "actual": []}

    data[date]["actual"].append({
        "task": task,
        "time": time
    })

    save_schedule(data)
