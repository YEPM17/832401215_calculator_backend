def test_calculate_success_and_persist(client):
    response = client.post("/api/calculate", json={"expression": "(1+2)*3"})
    history = client.get("/api/history")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "expression": "(1+2)*3",
        "result": 9.0,
    }
    assert history.status_code == 200
    assert history.json()["items"][0]["expression"] == "(1+2)*3"


def test_calculate_empty_expression(client):
    response = client.post("/api/calculate", json={"expression": "   "})

    assert response.status_code == 400
    assert response.json() == {
        "success": False,
        "message": "Expression cannot be empty",
    }


def test_calculate_division_by_zero(client):
    response = client.post("/api/calculate", json={"expression": "1/0"})

    assert response.status_code == 400
    assert response.json()["message"] == "Division by zero"


def test_calculate_requires_expression_field(client):
    response = client.post("/api/calculate", json={})

    assert response.status_code == 422
