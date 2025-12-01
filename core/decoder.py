# core/decoder.py

def decoder_behaviors(latent):
    """
    Convert latent-state info into user-facing suggestions.
    """

    suggestions = []

    # Emotional state
    emotion = latent.get("emotion")
    if emotion == "happy":
        suggestions.append("Sounds like things are really clicking for you — keep riding that momentum! 🚀")
    elif emotion == "sad":
        suggestions.append("I'm here with you. Want to talk about what's pulling you down?")
    elif emotion == "anxious":
        suggestions.append("Let's slow down for a moment. Deep breath. What's the biggest thought in your head right now?")
    
    # Stress
    stress = latent.get("stress_level")
    if stress == "high":
        suggestions.append("Maybe take a 2-minute pause. Your mind deserves a breather.")
    elif stress == "low" and emotion == "happy":
        suggestions.append("Low stress + positive emotion = perfect time to make a small step toward a goal.")

    # Needs
    needs = latent.get("needs")
    if needs and needs != "unknown":
        suggestions.append(f"It seems like you might need: **{needs}**.")

    # Goals
    goals = latent.get("goals")
    if goals and goals != "unknown":
        suggestions.append(f"Do you want to take a tiny action toward: **{goals}**?")

    # Fallback
    if not suggestions:
        suggestions.append("I'm here — tell me more about what's on your mind.")

    return suggestions
