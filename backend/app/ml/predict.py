"""
Loads the trained RandomForest model + label encoder + feature list once,
then exposes predict_diseases() to turn a list of symptom strings into a
ranked list of {disease, confidence, ...} results.
"""
import os
import json
import difflib
from functools import lru_cache
import numpy as np
import pandas as pd
import joblib

from app.ml.disease_info import get_disease_info

ARTIFACT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")


@lru_cache(maxsize=1)
def _load_artifacts():
    model = joblib.load(os.path.join(ARTIFACT_DIR, "disease_model.joblib"))
    encoder = joblib.load(os.path.join(ARTIFACT_DIR, "label_encoder.joblib"))
    with open(os.path.join(ARTIFACT_DIR, "feature_columns.json")) as f:
        feature_columns = json.load(f)
    return model, encoder, feature_columns


def get_all_symptoms() -> list:
    """Returns the full ordered list of symptom names the model understands."""
    _, _, feature_columns = _load_artifacts()
    return feature_columns


def normalize_symptom(raw: str, feature_columns: list) -> str | None:
    """Maps a loosely-typed symptom string to the closest known feature name."""
    cleaned = raw.strip().lower().replace(" ", "_")
    if cleaned in feature_columns:
        return cleaned
    matches = difflib.get_close_matches(cleaned, feature_columns, n=1, cutoff=0.7)
    return matches[0] if matches else None


def predict_diseases(symptoms: list, top_k: int = 5) -> list:
    """
    symptoms: list of raw symptom strings (free text or picked from list).
    Returns top_k ranked predictions:
      [{"disease", "confidence" (0-100), "specialist", "medicine_categories",
        "summary", "emergency"}]
    """
    model, encoder, feature_columns = _load_artifacts()

    matched = set()
    unmatched = []
    for s in symptoms:
        norm = normalize_symptom(s, feature_columns)
        if norm:
            matched.add(norm)
        else:
            unmatched.append(s)

    if not matched:
        return []

    vector = pd.DataFrame([[1 if col in matched else 0 for col in feature_columns]], columns=feature_columns)
    probabilities = model.predict_proba(vector)[0]

    ranked_idx = np.argsort(probabilities)[::-1][:top_k]
    results = []
    for idx in ranked_idx:
        disease = encoder.inverse_transform([idx])[0]
        confidence = round(float(probabilities[idx]) * 100, 1)
        if confidence <= 0:
            continue
        info = get_disease_info(disease)
        results.append({
            "disease": disease.strip(),
            "confidence": confidence,
            "specialist": info["specialist"],
            "medicine_categories": info["medicine_categories"],
            "summary": info["summary"],
            "emergency": info["emergency"],
        })

    return results


def get_unmatched_symptoms(symptoms: list) -> list:
    _, _, feature_columns = _load_artifacts()
    return [s for s in symptoms if normalize_symptom(s, feature_columns) is None]
