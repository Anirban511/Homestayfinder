def _create_place(client, headers):
    return client.post("/api/places", headers=headers, json={
        "title": "Cozy Cabin", "address": "Darjeeling", "description": "Hill views",
        "price": 50.0, "max_guests": 4,
    })


def test_create_and_list_place(client, auth_headers):
    res = _create_place(client, auth_headers)
    assert res.status_code == 201
    res = client.get("/api/places")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_search_places(client, auth_headers):
    _create_place(client, auth_headers)
    client.post("/api/places", headers=auth_headers, json={
        "title": "Beach House", "address": "Goa", "price": 200.0, "max_guests": 6,
    })
    # keyword
    res = client.get("/api/places/search", params={"q": "darjeeling"})
    assert len(res.json()) == 1
    # price filter
    res = client.get("/api/places/search", params={"max_price": 100})
    assert len(res.json()) == 1
