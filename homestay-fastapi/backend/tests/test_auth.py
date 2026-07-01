def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_register_and_login(client):
    res = client.post("/api/auth/register",
                      json={"name": "Bob", "email": "bob@example.com", "password": "pw12345"})
    assert res.status_code == 201
    res = client.post("/api/auth/login",
                      json={"email": "bob@example.com", "password": "pw12345"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_wrong_password(client):
    client.post("/api/auth/register",
                json={"name": "Cara", "email": "cara@example.com", "password": "pw12345"})
    res = client.post("/api/auth/login",
                      json={"email": "cara@example.com", "password": "wrong"})
    assert res.status_code == 401
