import os
import time

from app import create_app


def _make_client():
    os.environ["AUTO_OFF_SECONDS"] = "1"
    os.environ["DEFAULT_MODE"] = "auto"
    os.environ["MANUAL_OVERRIDE_SECONDS"] = "2"
    app = create_app()
    return app.test_client()


def test_set_brightness_updates_state():
    client = _make_client()
    response = client.post("/brightness", json={"brightness": 70})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["data"]["status"] == "success"
    assert payload["data"]["brightness"] == 70

    status = client.get("/light/status").get_json()
    assert status["data"]["brightness"] == 70
    assert "timer" in status["data"]
    assert "sensitivity" in status["data"]


def test_set_sensitivity_normalizes_and_persists():
    client = _make_client()
    response = client.post("/sensitivity", json={"sensitivity": "High"})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["data"]["sensitivity"] == "high"

    status = client.get("/light/status").get_json()
    assert status["data"]["sensitivity"] == "high"


def test_set_timer_changes_auto_off_duration():
    client = _make_client()

    timer_response = client.post("/timer", json={"timer": 5})
    assert timer_response.status_code == 200
    timer_payload = timer_response.get_json()
    assert timer_payload["data"]["timer"] == 5

    client.post("/bridge/motion-event", json={"detected": True})
    time.sleep(5.2)
    status_payload = client.get("/light/status").get_json()
    assert status_payload["data"]["power"] == "off"
    assert status_payload["data"]["mode"] == "auto"
    assert status_payload["data"]["timer"] == 5


def test_timer_rejects_invalid_values():
    client = _make_client()
    response = client.post("/timer", json={"timer": 12})
    assert response.status_code == 422
    payload = response.get_json()
    assert payload["success"] is False
