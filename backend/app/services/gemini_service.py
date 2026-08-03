"""
Gemini integration for the qualitative layer of the diagnosis pipeline:
  1. Parsing free-text symptom descriptions into structured symptom tags
     (matched against the ML model's known symptom vocabulary)
  2. Generating a plain-language explanation of the ML model's ranked
     predictions, including general-category guidance and red-flag warnings
  3. Never outputs specific drug names/dosages — only general categories,
     and always defers to a licensed professional for anything prescriptive.

Falls back to deterministic templates if no GEMINI_API_KEY is set, so the
app remains demoable without a paid key.
"""
import json
import re
from typing import Optional
from functools import lru_cache
from google import genai
from app.core.config import settings


@lru_cache(maxsize=1)
def _get_client():
    if not settings.GEMINI_API_KEY:
        return None
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def _extract_json(text: str):
    cleaned = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    return json.loads(cleaned)


def _call_gemini(prompt: str) -> Optional[str]:
    client = _get_client()
    if client is None:
        return None
    response = client.models.generate_content(model=settings.GEMINI_MODEL, contents=prompt)
    return response.text


def parse_free_text_symptoms(free_text: str, known_symptoms: list) -> list:
    """Extracts likely symptom tags (from the model's known vocabulary) from free text."""
    prompt = f"""A patient described their symptoms in their own words:
"{free_text}"

Here is the list of symptom terms our system recognizes:
{json.dumps(known_symptoms)}

Return ONLY a JSON array of the recognized symptom terms (exact strings from the
list above) that best match what the patient described. Include only terms that
are clearly present. Example: ["itching", "skin_rash", "fatigue"]
"""
    raw = _call_gemini(prompt)
    if raw is None:
        # Naive offline fallback: substring match against known vocabulary
        text_lower = free_text.lower()
        return [s for s in known_symptoms if s.replace("_", " ") in text_lower]
    try:
        parsed = _extract_json(raw)
        return [s for s in parsed if s in known_symptoms]
    except Exception:
        return []


def generate_explanation(predictions: list, patient_context: dict) -> dict:
    """
    predictions: ranked ML output (list of dicts with disease/confidence/etc).
    patient_context: {age, sex, duration_days, severity, symptoms}
    Returns {explanation, red_flags: [str]}
    """
    prompt = f"""You are a careful, cautious medical information assistant (NOT a doctor).
A machine learning model analyzed a patient's symptoms and produced this ranked list
of possible conditions with confidence scores:

{json.dumps(predictions, indent=2)}

Patient context: {json.dumps(patient_context)}

Write a short (4-6 sentence), plain-language, reassuring-but-honest explanation of
these results for the patient. Rules:
- Never state a definitive diagnosis — always frame results as possibilities to discuss with a doctor.
- Do not mention specific drug names or dosages.
- If any listed condition is flagged emergency=true, or the symptoms/context suggest
  something urgent, clearly state that they should seek immediate/emergency care.
- End by recommending they consult the suggested specialist type for a proper evaluation.

Return ONLY JSON in this shape:
{{
  "explanation": "...",
  "red_flags": ["short red-flag warning if applicable", "..."]
}}
"""
    raw = _call_gemini(prompt)
    if raw is None:
        top = predictions[0] if predictions else None
        emergency_flag = any(p.get("emergency") for p in predictions)
        explanation = (
            f"Based on the symptoms you reported, the most likely possibility our model "
            f"identified is {top['disease']} (confidence: {top['confidence']}%), though "
            f"several other conditions share overlapping symptoms. This is not a diagnosis — "
            f"please consult a {top['specialist']} to confirm and get proper treatment."
            if top else
            "We couldn't confidently match your symptoms to a condition in our database. "
            "Please consult a general physician for a full evaluation."
        )
        red_flags = (
            ["One or more predicted conditions can be serious — seek medical attention promptly."]
            if emergency_flag else []
        )
        return {"explanation": explanation, "red_flags": red_flags}

    try:
        return _extract_json(raw)
    except Exception:
        return {
            "explanation": "Your results were generated, but a detailed AI summary is unavailable this run.",
            "red_flags": [],
        }
