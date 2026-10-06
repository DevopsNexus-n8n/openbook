from .conftest import signup


def test_signup_creates_tenant_and_me_returns_it(client):
    headers = signup(client)
    r = client.get("/api/me", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["email"] == "owner@example.com"
    assert body["role"] == "owner"
    assert body["tenant"]["name"] == "Glow Salon"
    assert body["tenant"]["plan"] == "trial"
    assert body["tenant"]["trial_ends_at"] is not None


def test_two_businesses_are_separate(client):
    a = client.get("/api/me", headers=signup(client, "Glow Salon", "a@example.com")).json()
    b = client.get("/api/me", headers=signup(client, "Glow Salon", "b@example.com")).json()
    assert a["tenant"]["id"] != b["tenant"]["id"]
    assert a["tenant"]["slug"] != b["tenant"]["slug"]


def test_duplicate_email_rejected(client):
    signup(client)
    r = client.post("/api/auth/signup", json={"business_name": "Other", "email": "OWNER@example.com", "password": "a-long-password"})
    assert r.status_code == 409


def test_short_password_rejected(client):
    r = client.post("/api/auth/signup", json={"business_name": "Glow", "email": "x@example.com", "password": "short"})
    assert r.status_code == 422


def test_login_success_and_failure(client):
    signup(client)
    ok = client.post("/api/auth/login", json={"email": "owner@example.com", "password": "a-long-password"})
    assert ok.status_code == 200 and ok.json()["token_type"] == "bearer"
    bad = client.post("/api/auth/login", json={"email": "owner@example.com", "password": "wrong-password"})
    assert bad.status_code == 401
    ghost = client.post("/api/auth/login", json={"email": "nobody@example.com", "password": "a-long-password"})
    assert ghost.status_code == 401
    assert bad.json() == ghost.json()  # same message, so emails can't be probed


def test_me_requires_valid_token(client):
    assert client.get("/api/me").status_code == 401
    assert client.get("/api/me", headers={"Authorization": "Bearer garbage"}).status_code == 401
