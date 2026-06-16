from fastapi.testclient import TestClient

from basebender.api.main import APP

client = TestClient(APP)


def test_root_redirects_to_docs():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert "/docs" in response.headers["location"]


def test_list_digit_sets():
    response = client.get("/digitsets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "name" in data[0]
    assert "digits" in data[0]
    assert "source" in data[0]


def test_rebase_binary_to_decimal():
    response = client.post(
        "/rebase",
        json={
            "input_text": "101",
            "source_digit_set_id": "package:Binary",
            "target_digit_set_id": "package:Decimal",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["rebased_text"] == "5"
    assert data["error"] is None


def test_rebase_with_direct_strings():
    response = client.post(
        "/rebase",
        json={
            "input_text": "hello",
            "source_digit_set": "abcdefghijklmnopqrstuvwxyz",
            "target_digit_set": "01",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] is None
    assert isinstance(data["rebased_text"], str)


def test_rebase_invalid_source_id():
    response = client.post(
        "/rebase",
        json={
            "input_text": "101",
            "source_digit_set_id": "package:NonExistent",
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert "Invalid" in data["detail"]["message"] or "not found" in data["detail"]["detail"]


def test_rebase_invalid_target_id():
    response = client.post(
        "/rebase",
        json={
            "input_text": "101",
            "target_digit_set_id": "package:NonExistent",
        },
    )
    assert response.status_code == 400


def test_rebase_empty_input():
    response = client.post(
        "/rebase",
        json={"input_text": ""},
    )
    assert response.status_code == 200


def test_rebase_no_digit_sets_dynamic():
    response = client.post(
        "/rebase",
        json={"input_text": "hello"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["rebased_text"] == "hello"
