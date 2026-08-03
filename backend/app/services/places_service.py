"""
Looks up nearby doctors/clinics matching a given specialty using the Google
Places API (Nearby Search + Text Search). Requires GOOGLE_PLACES_API_KEY.
If no key is configured, returns an empty result set with a helpful note
instead of failing, so the rest of the app remains usable in a demo/offline
setting.
"""
import httpx
from app.core.config import settings

PLACES_TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"


def find_nearby_specialists(specialty: str, latitude: float, longitude: float, radius_m: int = 15000) -> dict:
    if not settings.GOOGLE_PLACES_API_KEY:
        return {
            "specialty_searched": specialty,
            "results": [],
            "note": (
                "Nearby specialist search requires a GOOGLE_PLACES_API_KEY to be configured "
                "in the backend .env file. See README for setup instructions."
            ),
        }

    # Use the first specialty listed if multiple are comma-separated (e.g. "ENT specialist / Neurologist")
    primary_specialty = specialty.split("/")[0].strip()

    params = {
        "query": f"{primary_specialty} near me",
        "location": f"{latitude},{longitude}",
        "radius": radius_m,
        "key": settings.GOOGLE_PLACES_API_KEY,
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(PLACES_TEXT_SEARCH_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPError as e:
        return {
            "specialty_searched": specialty,
            "results": [],
            "note": f"Could not reach the Places API: {e}",
        }

    results = []
    for place in data.get("results", [])[:8]:
        results.append({
            "name": place.get("name", "Unknown"),
            "address": place.get("formatted_address", ""),
            "rating": place.get("rating"),
            "specialty": primary_specialty,
            "distance_km": None,  # Text Search doesn't return distance directly
            "place_id": place.get("place_id"),
        })

    return {"specialty_searched": primary_specialty, "results": results, "note": None}
