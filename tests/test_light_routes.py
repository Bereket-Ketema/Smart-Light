import os

from app import create_app


def _make_client():
    os.environ["AUTO_OFF_SECONDS"] = "1"
    os.environ["DEFAULT_MODE"] = "auto"
    os.environ["MANUAL_OVERRIDE_SECONDS"] = "2"
    app = create_app()
    return app.test_client()


def test_light_status_shape():
    client = _make_client()
    response = client.get("/light/status")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["data"]["power"] in {"on", "off"}
    assert payload["data"]["mode"] in {"auto", "manual"}


def test_manual_on_and_off():
    client = _make_client()

    on_response = client.post("/light/on")
    assert on_response.status_code == 200
    on_payload = on_response.get_json()
    assert on_payload["data"]["power"] == "on"
    assert on_payload["data"]["mode"] == "manual"

    off_response = client.post("/light/off")
    assert off_response.status_code == 200
    off_payload = off_response.get_json()
    assert off_payload["data"]["power"] == "off"
    assert off_payload["data"]["mode"] == "manual"
