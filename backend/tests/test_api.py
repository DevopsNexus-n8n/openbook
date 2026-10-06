def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_waitlist_is_idempotent(client):
    for _ in range(2):
        r = client.post("/api/waitlist", json={"email": "Owner@Example.com", "business_type": "salon"})
        assert r.status_code == 200
        assert r.json() == {"ok": True}


def test_waitlist_rejects_bad_email(client):
    r = client.post("/api/waitlist", json={"email": "not-an-email"})
    assert r.status_code == 422
