import pytest
from fastapi.testclient import TestClient
from app import app  # Assuming your FastAPI instance is in app.main
from products_app.models import Product  # Import your Product model from the correct location

client = TestClient(app)


def test_get_products():
    response = client.get("/api/products")
    assert response.status_code == 200

    # Check that the response is a list
    assert isinstance(response.json(), list)

    # Validate each item in the response list against the Product model
    for item in response.json():
        product = Product.parse_obj(item)
        assert isinstance(product, Product)

    # Optionally, assert specific properties of the first item
    first_product = response.json()[0]
    assert "displayName" in first_product
    assert "price" in first_product
    assert "category" in first_product
    assert isinstance(first_product["displayName"], str)
    assert isinstance(first_product["price"], str)
