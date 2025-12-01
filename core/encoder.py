from datetime import datetime

# === Dimensional schema ===
DIMENSION_LIST = [
    "identity",
    "emotion",
    "intention",
    "time",
    "context",
    "self_reflection",
    "behavior",
    "needs",
    "stress_level",
    "goals",
    "meta_stability",
    "social_self"
]


def encode_entry(text: str, llm_output: dict):
    """
    Convert raw text + LLM JSON output into a structured multi-dimensional entry.
    """

    encoded = {
        "timestamp": datetime.now().isoformat(),
        "raw": text,
        "latent": {}
    }

    # Fill latent dimensions
    for dim in DIMENSION_LIST:
        encoded["latent"][dim] = llm_output.get(dim, None)

    return encoded
