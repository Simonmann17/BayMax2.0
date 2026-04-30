import anthropic
import json
from app.core.config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """
You are BayMax, a compassionate medical triage assistant. 
Your only job is to assess reported symptoms and recommend 
one of three actions. You are NOT a doctor and must NEVER 
diagnose a condition or recommend specific medications. 


Based on the symptoms provided, you must respond with a JSON 
object in exactly the following format and nothing else:

{
    "urgency_level": "emergency" or "see_doctor" or "home_care",
    "recommendation": "One sentence telling the user what to do",
    "reasoning": "Two to three sentences explaining why, based only on the symptoms described",
    "disclaimer": "This is not a medical diagnosis. "
    "Please consult a qualified healthcare professional for proper medical advice."
}

Rules you must follow:
- Never suggest a specific diagnosis or condition name
- Never recommend specific medications or dosages
- If symptoms suggest any risk to life, always return emergency
- If you are uncertain, always escalate to the higher urgency level
- Respond with the JSON object only, no preamble, no markdown, no code fences, no explanation outside the JSON
"""


def get_triage(
        symptom: str,
        duration: str,
        severity: int,
        age: int,
        details: str = None,
        known_conditions: str = None
) -> dict:
    user_message = f"""
    Patient reported symptoms:
    - Primary symptom: {symptom}
    - Duration: {duration}
    - Severity (1-10): {severity}
    - Age: {age}
    - Additional details: {details or 'None provided'}
    - Known medical conditions: {known_conditions or 'None provided'}
    """

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )

    response_text = message.content[0].text.strip()
    if response_text.startswith("```"):
        response_text = response_text.split("\n", 1)[1]
    if response_text.endswith("```"):
        response_text = response_text.rsplit("\n", 1)[0]
    print("RAW REPONSE:", response_text)

    try:
        triage_result = json.loads(response_text)
    except json.JSONDecodeError:
        triage_result = {
            "urgency_level": "see_doctor",
            "recommendation": "Unable to assess symptoms. Please consult a healthcare professional.",
            "reasoning": "A technical error occurred during assessment.",
            "disclaimer": "This is not a medical diagnosis. "
            "Please consult a qualified healthcare professional for proper medical advice."
        }
    return triage_result
