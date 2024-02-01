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

    response = client.post("/urls/", json={"long_url": "https://youtube.com"})
    assert response.status_code == 200
    assert response.json()["long_url"] == "https://youtube.com"
    assert response.json()["short_url"] == "2"


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


def test_create_short_url_with_existing_long_url(client: TestClient):
    first_response = client.post("/urls/", json={"long_url": "https://google.com"})
    first_json_response = first_response.json()

    duplicate_response = client.post("/urls/", json={"long_url": "https://google.com"})
    duplicate_json_response = duplicate_response.json()

    assert first_json_response == duplicate_json_response


def test_create_short_url_with_existing_custom_short_url(client: TestClient):
    client.post(
        "/urls/",
        json={
            "long_url": "https://google.com",
            "short_url": "asdfgh",
        },
    )

    second_response = client.post(
        "/urls/",
        json={
            "long_url": "https://google.com",
            "short_url": "asdfgh",
        },
    )
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Custom short URL already exists"


@pytest.mark.skip
def test_very_long_url():
    pass


@pytest.mark.skip
def test_very_long_custom_url():
    pass


def test_empty_string_custom_url(client: TestClient):
    response = client.post(
        "/urls/",
        json={
            "long_url": "https://google.com",
            "short_url": "",
        },
    )

    assert response.status_code == 422


def test_only_whitespace_string_custom_url(client: TestClient):
    response = client.post(
        "/urls/",
        json={
            "long_url": "https://google.com",
            "short_url": " ",
        },
    )

    assert response.status_code == 422


def test_with_whitespace_string_custom_url(client: TestClient):
    response = client.post(
        "/urls/",
        json={
            "long_url": "https://google.com",
            "short_url": " asdf ",
        },
    )

    assert response.status_code == 422
