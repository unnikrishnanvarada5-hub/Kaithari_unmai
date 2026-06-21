"""
Optional generative layer: turns the raw match result into a short,
warm heritage note using Groq's LLaMA models. Purely additive -- if the
API key is missing or the call fails for any reason, the app silently
falls back to the static REGION_INFO note, so the core verification
feature never depends on this.
"""

from groq import Groq

# Hardcoded for local/dev convenience -- replace with your own key.
# Get a free key at https://console.groq.com/keys
GROQ_API_KEY = "your-groq-api-key-here"

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def generate_heritage_note(region_display_name: str, state: str, motif: str) -> str | None:
    """Returns a 2-3 sentence heritage note, or None if generation fails."""
    if not GROQ_API_KEY or GROQ_API_KEY == "your-groq-api-key-here":
        return None

    prompt = (
        f"In 2-3 warm, specific sentences, describe the handloom weaving "
        f"tradition of {region_display_name} from {state}, India. "
        f"Mention this signature characteristic naturally: {motif}. "
        f"Write for someone who just verified a saree's pattern and wants "
        f"to understand its heritage. No headers, no bullet points, plain prose."
    )

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=180,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None
