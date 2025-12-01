# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 20:55:10 2025

@author: chris
"""

import json
from datetime import datetime, timedelta

def load_entries(path="journal.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# ------------------------------------------------------------
# 1. Detect habit frequency
# ------------------------------------------------------------
def detect_habit_frequency(entries, habit_name):
    count = 0
    for entry in entries:
        latent = entry["latent"]
        if latent.get("behavior") == habit_name:
            count += 1
    return count


# ------------------------------------------------------------
# 2. Detect time-of-day patterns
# ------------------------------------------------------------
def detect_time_pattern(entries):
    times = []
    for entry in entries:
        ts = datetime.fromisoformat(entry["timestamp"])
        times.append(ts.hour)

    if not times:
        return None

    # Most common hour
    return max(set(times), key=times.count)


# ------------------------------------------------------------
# 3. Detect streaks (good or bad habits)
# ------------------------------------------------------------
def habit_streak(entries, habit_name):
    streak = 0
    today = datetime.now().date()

    # Reverse chronological
    for entry in reversed(entries):
        latent = entry["latent"]
        if latent.get("behavior") != habit_name:
            break

        entry_date = datetime.fromisoformat(entry["timestamp"]).date()
        if (today - entry_date).days == streak:
            streak += 1
        else:
            break

    return streak


# ------------------------------------------------------------
# 4. Grounding cue detection
# ------------------------------------------------------------
def detect_grounding_needed(entry):
    latent = entry["latent"]

    # Simple rules for now
    if latent.get("stress_level") == "high":
        return True
    
    if latent.get("emotion") in ["anxious", "overwhelmed"]:
        return True

    return False


# ------------------------------------------------------------
# 5. “Good timing” prediction
# ------------------------------------------------------------
def predict_next_habit_time(entries, habit_name):
    """
    Very simple version:
    Look at timestamps where the habit occurs.
    Return the average “hour of day.”
    """
    hours = []

    for entry in entries:
        latent = entry["latent"]
        if latent.get("behavior") == habit_name:
            ts = datetime.fromisoformat(entry["timestamp"])
            hours.append(ts.hour)

    if not hours:
        return None

    avg_hour = sum(hours) / len(hours)
    return int(avg_hour)
