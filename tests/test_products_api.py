import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_products():
    response = client.get("/api/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
