def test_booking_and_payment_flow(client, auth_headers):
    place = client.post("/api/places", headers=auth_headers, json={
        "title": "Loft", "address": "Gangtok", "price": 100.0, "max_guests": 2,
    }).json()

    booking = client.post("/api/bookings", headers=auth_headers, json={
        "place_id": place["id"],
        "check_in": "2026-07-01T00:00:00",
        "check_out": "2026-07-04T00:00:00",
        "guests": 2,
    }).json()
    assert booking["price"] == 300.0          # 3 nights * 100
    assert booking["payment_status"] == "unpaid"

    intent = client.post("/api/payments/create-intent", headers=auth_headers,
                         json={"booking_id": booking["id"]}).json()
    assert intent["mode"] == "stub"

    res = client.post("/api/payments/confirm", headers=auth_headers,
                     json={"payment_id": intent["payment_id"]})
    assert res.status_code == 200

    # Booking should now be confirmed + paid.
    mine = client.get("/api/bookings", headers=auth_headers).json()
    assert mine[0]["status"] == "confirmed"
    assert mine[0]["payment_status"] == "paid"
