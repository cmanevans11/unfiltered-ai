# core/task_placement.py

from datetime import datetime, timedelta
from .schedule_memory import load_schedule, save_schedule


def _hour_to_int(hhmm):
    """Convert HH:MM to integer hour 0–23."""
    return int(hhmm.split(":")[0])


def _find_common_hours(actual_tasks):
    """Return the hours during which the user is usually active."""
    hour_counts = {}

    for task in actual_tasks:
        time = task.get("time")
        if not time:
            continue

        hour = _hour_to_int(time)

        if hour not in hour_counts:
            hour_counts[hour] = 0
        hour_counts[hour] += 1

    # Return hours sorted by frequency
    return sorted(hour_counts, key=lambda h: hour_counts[h], reverse=True)


def _best_hour_for_task(preferred_hours, planned_tasks):
    """Pick the highest-ranked hour that does NOT conflict."""
    used_hours = {_hour_to_int(p["start"]) for p in planned_tasks}

    for hour in preferred_hours:
        if hour not in used_hours:
            return hour

    # If every hour is used, choose next available
    for hour in range(24):
        if hour not in used_hours:
            return hour

    return None  # very unlikely


def auto_place_task(task_name, duration_minutes=45):
    """
    Automatically schedule a task based on past behavior.
    """

    schedule = load_schedule()
    today = datetime.now().date().isoformat()

    if today not in schedule:
        schedule[today] = {"planned": [], "actual": []}

    actual = schedule[today]["actual"]
    planned = schedule[today]["planned"]

    # 1. Detect user's natural activity windows
    natural_hours = _find_common_hours(actual)

    # If no activity yet → place task at current time
    if not natural_hours:
        start = datetime.now().strftime("%H:%M")
        end_time = (datetime.now() + timedelta(minutes=duration_minutes)).strftime("%H:%M")

        schedule[today]["planned"].append({
            "task": task_name,
            "start": start,
            "end": end_time
        })

        save_schedule(schedule)
        return f"Scheduled '{task_name}' immediately at {start}."


    # 2. Choose best hour based on natural windows
    best_hour = _best_hour_for_task(natural_hours, planned)

    start_time = f"{best_hour:02d}:00"
    end_time = (datetime.strptime(start_time, "%H:%M") +
                timedelta(minutes=duration_minutes)).strftime("%H:%M")

    schedule[today]["planned"].append({
        "task": task_name,
        "start": start_time,
        "end": end_time
    })

    save_schedule(schedule)

    return f"Scheduled '{task_name}' at your natural activity time: {start_time}."
