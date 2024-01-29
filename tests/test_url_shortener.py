import pytest
from fastapi.testclient import TestClient


def test_index(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "pong"


def test_non_existent_url(client: TestClient):
    response = client.get("/abcdef")
    assert response.status_code == 404


def test_empty_urls(client: TestClient):
    response = client.get("/urls/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_one_short_url(client: TestClient):
    response = client.post("/urls/", json={"long_url": "https://google.com"})

    assert response.status_code == 200
    assert response.json()["long_url"] == "https://google.com"
    assert response.json()["short_url"] == "1"


def test_create_two_short_url(client: TestClient):
    response = client.post("/urls/", json={"long_url": "https://google.com"})

    assert response.status_code == 200
    assert response.json()["long_url"] == "https://google.com"
    assert response.json()["short_url"] == "1"


def test_get_non_existent_short_url(client: TestClient):
    short_url = "non-existent"
    response = client.get(f"/urls/{short_url}")
    assert response.status_code == 404


def test_create_and_check_short_url(client: TestClient):
    response = client.post("/urls/", json={"long_url": "https://google.com"})

    assert response.status_code == 200
    assert response.json()["long_url"] == "https://google.com"
    assert response.json()["short_url"] == "1"

    short_url = response.json()["short_url"]
    long_url = response.json()["long_url"]
    response = client.get(f"/urls/{short_url}")

    assert response.status_code == 200
    assert response.json()["short_url"] == short_url
    assert response.json()["long_url"] == long_url


def test_create_one_custom_short_url(client: TestClient):
    response = client.post(
        "/urls/",
        json={
            "long_url": "https://google.com",
            "short_url": "asdfgh",
        },
    )
    
    assert response.status_code == 200
    assert response.json()["long_url"] == "https://google.com"
    assert response.json()["short_url"] == "asdfgh"


@pytest.mark.skip(reason="Not implemented")
def test_create_short_url_with_existing_long_url(client: TestClient):
    assert False


@pytest.mark.skip(reason="Not implemented")
def test_create_short_url_with_existing_custom_short_url(client: TestClient):
    assert False
