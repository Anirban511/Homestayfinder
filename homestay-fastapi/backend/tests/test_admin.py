from app.models import User
from tests.conftest import TestingSessionLocal, register_and_login


def _make_admin(email):
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == email).first()
    user.role = "admin"
    db.commit()
    db.close()


def test_admin_requires_role(client, auth_headers):
    # A normal (non-admin) user is forbidden.
    res = client.get("/api/admin/stats", headers=auth_headers)
    assert res.status_code == 403


def test_admin_stats_and_analytics(client):
    headers = register_and_login(client, name="Admin", email="admin@example.com", password="pw12345")
    _make_admin("admin@example.com")
    # The role guard reads the DB user fresh, so the existing token now resolves
    # to an admin without needing to re-login.
    res = client.get("/api/admin/stats", headers=headers)
    assert res.status_code == 200
    assert res.json()["users"] == 1

    res = client.get("/api/admin/analytics", headers=headers)
    assert res.status_code == 200
    assert "bookings_by_status" in res.json()
