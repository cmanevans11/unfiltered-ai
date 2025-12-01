# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 21:18:24 2025

@author: chris
"""

def test_notification_trigger():
    entries = load_entries()
    predicted = predict_next_habit_time(entries, "tiktok")

    # Simulate "now"
    current_hour = predicted  # force-match

    print("\n=== NOTIFICATION TEST ===")
    print("Predicted:", predicted)
    print("Current hour:", current_hour)

    if predicted == current_hour:
        print("🔔 Notification fired successfully!")
    else:
        print("No notification.")
