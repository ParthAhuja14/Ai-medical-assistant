def test_register_and_login(client):
    resp = client.post("/api/auth/register", json={
        "full_name": "Alice Example",
        "email": "alice_auth_test@example.com",
        "password": "supersecret",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["user"]["email"] == "alice_auth_test@example.com"
    assert "access_token" in data

    login_resp = client.post("/api/auth/login", data={
        "username": "alice_auth_test@example.com",
        "password": "supersecret",
    })
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()


def test_register_duplicate_email_rejected(client):
    payload = {"full_name": "Bob", "email": "bob_dup_test@example.com", "password": "password123"}
    first = client.post("/api/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/api/auth/register", json=payload)
    assert second.status_code == 400


def test_login_wrong_password_rejected(client):
    client.post("/api/auth/register", json={
        "full_name": "Carol", "email": "carol_test@example.com", "password": "correcthorse",
    })
    resp = client.post("/api/auth/login", data={
        "username": "carol_test@example.com", "password": "wrongpassword",
    })
    assert resp.status_code == 401


def test_me_requires_auth(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_me_returns_current_user(client, auth_headers):
    resp = client.get("/api/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert "email" in resp.json()
