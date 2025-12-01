# core/prediction.py

from datetime import datetime
from .schedule_memory import load_schedule


def _hour_to_int(hhmm):
    return int(hhmm.split(":")[0])


def get_common_distraction_hours(data):
    """Returns the hours where non-productive tasks appear."""
    distraction_hours = {}

    for date, info in data.items():
        for task in info.get("actual", []):
            name = task.get("task", "").lower()
            if name in ["tiktok", "instagram", "youtube", "scrolling"]:
                hour = _hour_to_int(task["time"])
                distraction_hours[hour] = distraction_hours.get(hour, 0) + 1

    return sorted(distraction_hours, key=lambda h: distraction_hours[h], reverse=True)


def get_common_productive_hours(data):
    """Returns the hours where user tends to work or focus."""
    productive_hours = {}

    KEYWORDS = ["coding", "studying", "writing", "work", "learning"]

    for date, info in data.items():
        for task in info.get("actual", []):
            name = task.get("task", "").lower()

            if any(k in name for k in KEYWORDS):
                hour = _hour_to_int(task["time"])
                productive_hours[hour] = productive_hours.get(hour, 0) + 1

    return sorted(productive_hours, key=lambda h: productive_hours[h], reverse=True)


def predict_best_focus_time():
    data = load_schedule()

    if not data:
        return None

    common = get_common_productive_hours(data)
    return common[0] if common else None


def predict_biggest_distraction_time():
    data = load_schedule()

    if not data:
        return None

    common = get_common_distraction_hours(data)
    return common[0] if common else None


def summarize_patterns():
    """Return a human-readable summary of behavioral patterns."""
    data = load_schedule()

    focus = predict_best_focus_time()
    distract = predict_biggest_distraction_time()

    summary = []

    if focus is not None:
        summary.append(f"🟢 Your strongest focus time is around **{focus}:00**.")

    if distract is not None:
        summary.append(f"🔴 Your biggest distraction time is around **{distract}:00**.")

    if not summary:
        summary.append("Not enough data to detect patterns yet.")

    return summary
