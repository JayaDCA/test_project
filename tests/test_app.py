"""Tests for the Flask app routes. Some tests FAIL due to known bugs."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"CodeBenders" in r.data


def test_list_users_empty(client):
    r = client.get("/users")
    assert r.status_code == 200
    assert r.get_json()["success"] is True


def test_create_user_valid(client):
    r = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    assert r.status_code == 201


# FAILS: POST /users without fields causes KeyError 500 instead of 400
def test_create_user_missing_name(client):
    r = client.post("/users", json={"email": "alice@example.com"})
    assert r.status_code == 400  # BUG: currently 500
    assert "name" in r.get_json().get("error", "").lower()


# FAILS: POST /users without fields causes KeyError 500 instead of 400
def test_create_user_missing_email(client):
    r = client.post("/users", json={"name": "Bob"})
    assert r.status_code == 400  # BUG: currently 500
    assert "email" in r.get_json().get("error", "").lower()


def test_list_products_empty(client):
    r = client.get("/products")
    assert r.status_code == 200


def test_create_product_valid(client):
    r = client.post("/products", json={"name": "Widget", "price": 9.99})
    assert r.status_code == 201


# FAILS: adding duplicate product name causes AssertionError 500 instead of 409
def test_create_product_duplicate(client):
    client.post("/products", json={"name": "Gadget", "price": 5.00})
    r = client.post("/products", json={"name": "Gadget", "price": 5.00})
    assert r.status_code == 409  # BUG: currently 500


def test_stats(client):
    r = client.get("/stats")
    assert r.status_code == 200
    data = r.get_json()
    assert "users" in data
    assert "products" in data
