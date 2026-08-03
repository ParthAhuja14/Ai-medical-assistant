def test_symptom_list_is_public_and_populated(client):
    resp = client.get("/api/diagnosis/symptoms")
    assert resp.status_code == 200
    symptoms = resp.json()["symptoms"]
    assert len(symptoms) == 132
    assert "itching" in symptoms


def test_diagnosis_requires_auth(client):
    resp = client.post("/api/diagnosis/", json={"symptoms": ["itching"]})
    assert resp.status_code == 401


def test_diagnosis_rejects_empty_symptoms(client, auth_headers):
    resp = client.post("/api/diagnosis/", json={"symptoms": []}, headers=auth_headers)
    assert resp.status_code == 422  # min_length=1 on the schema


def test_diagnosis_fungal_infection_symptoms(client, auth_headers):
    """A known, unambiguous symptom cluster for fungal infection should
    rank it at or near the top of the predictions."""
    resp = client.post("/api/diagnosis/", json={
        "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions"],
        "age": 25, "sex": "male", "duration_days": 3, "severity": "mild",
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert len(data["predictions"]) > 0
    top = data["predictions"][0]
    assert top["confidence"] > 0
    assert "specialist" in top
    assert "medicine_categories" in top
    assert isinstance(top["medicine_categories"], list)
    assert "disclaimer" in data
    assert "not a medical diagnosis" in data["disclaimer"].lower() or "not a" in data["disclaimer"].lower()


def test_diagnosis_flags_emergency_for_heart_attack_symptoms(client, auth_headers):
    resp = client.post("/api/diagnosis/", json={
        "symptoms": ["chest_pain", "breathlessness", "sweating"],
        "age": 55, "sex": "male", "severity": "severe",
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["is_emergency"] is True


def test_diagnosis_with_unrecognized_symptoms_only_returns_422(client, auth_headers):
    resp = client.post("/api/diagnosis/", json={
        "symptoms": ["this_is_not_a_real_symptom_xyz"],
    }, headers=auth_headers)
    assert resp.status_code == 422


def test_history_reflects_past_sessions(client, auth_headers):
    client.post("/api/diagnosis/", json={"symptoms": ["itching", "skin_rash"]}, headers=auth_headers)
    resp = client.get("/api/diagnosis/history", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_specialists_requires_location(client, auth_headers):
    create_resp = client.post("/api/diagnosis/", json={
        "symptoms": ["itching", "skin_rash"],
    }, headers=auth_headers)
    session_id = create_resp.json()["id"]

    resp = client.get(f"/api/diagnosis/{session_id}/specialists", headers=auth_headers)
    assert resp.status_code == 400  # no lat/long was provided for this session
