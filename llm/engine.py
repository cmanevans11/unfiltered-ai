import json
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """
You are a structured-analysis engine for a journaling assistant.
Return ONLY a JSON object with the following keys:

time, emotion, intention, context, self_reflection,
behavior, needs, stress_level, goals
"""

def analyze_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"}
    )

    # The content is a JSON string — parse it
    json_str = response.choices[0].message.content
    return json.loads(json_str)
