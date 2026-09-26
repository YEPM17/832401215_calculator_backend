def test_history_is_newest_first_and_can_be_deleted(client):
    first = client.post("/api/calculate", json={"expression": "1+1"}).json()
    assert first["result"] == 2.0
    second = client.post("/api/calculate", json={"expression": "2+2"}).json()
    assert second["result"] == 4.0

    history = client.get("/api/history").json()["items"]
    assert [item["expression"] for item in history] == ["2+2", "1+1"]

    second_id = history[0]["id"]
    delete = client.delete(f"/api/history/{second_id}")
    assert delete.status_code == 204

    remaining = client.get("/api/history").json()["items"]
    assert [item["expression"] for item in remaining] == ["1+1"]


def test_delete_missing_history_returns_404(client):
    response = client.delete("/api/history/9999")

    assert response.status_code == 404
    assert response.json()["success"] is False


def test_clear_all_history(client):
    client.post("/api/calculate", json={"expression": "1+1"})
    client.post("/api/calculate", json={"expression": "2+2"})

    response = client.delete("/api/history")

    assert response.status_code == 204
    assert client.get("/api/history").json()["items"] == []


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
