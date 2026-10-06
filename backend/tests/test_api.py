import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


def test_health():
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


def test_waitlist_is_idempotent():
    with TestClient(app) as client:
        for _ in range(2):
            r = client.post("/api/waitlist", json={"email": "Owner@Example.com", "business_type": "salon"})
            assert r.status_code == 200
            assert r.json() == {"ok": True}


def test_waitlist_rejects_bad_email():
    with TestClient(app) as client:
        r = client.post("/api/waitlist", json={"email": "not-an-email"})
        assert r.status_code == 422
