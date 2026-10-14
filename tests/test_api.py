"""Basic API tests. Run with: pytest"""

import pytest
from fastapi.testclient import TestClient

from app import store
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_data():
    # Start every test from the same sample data
    store.reset()


def test_create_and_get():
    r = client.post("/contacts", json={"first_name": "Test", "last_name": "User"})
    assert r.status_code == 201
    contact_id = r.json()["id"]
    assert client.get(f"/contacts/{contact_id}").json()["first_name"] == "Test"


def test_create_requires_names_and_valid_email():
    assert client.post("/contacts", json={"first_name": "Only"}).status_code == 422
    bad_email = {"first_name": "A", "last_name": "B", "email": "not-an-email"}
    assert client.post("/contacts", json=bad_email).status_code == 422


def test_update_and_edit():
    body = {"first_name": "New", "last_name": "Name", "tags": ["Work"]}
    assert client.put("/contacts/1", json=body).json()["first_name"] == "New"
    r = client.patch("/contacts/1", json={"phone": "+90 555 000 0000"})
    assert r.json()["phone"] == "+90 555 000 0000"
    assert r.json()["first_name"] == "New"  # unchanged


def test_delete():
    assert client.delete("/contacts/1").status_code == 204
    assert client.get("/contacts/1").status_code == 404


def test_search_filter_and_sort():
    r = client.get("/contacts", params={"search": "turing"}).json()
    assert [c["last_name"] for c in r["items"]] == ["Turing"]

    r = client.get("/contacts", params={"tag": "work"}).json()
    assert all("Work" in c["tags"] for c in r["items"])

    names = [c["first_name"] for c in client.get("/contacts", params={"order": "desc"}).json()["items"]]
    assert names == sorted(names, reverse=True)


def test_pagination():
    r = client.get("/contacts", params={"page_size": 3, "page": 2}).json()
    assert len(r["items"]) == 3 and r["total"] == 8


def test_toggle_favorite():
    before = client.get("/contacts/2").json()["is_favorite"]
    assert client.patch("/contacts/2/favorite").json()["is_favorite"] is not before
