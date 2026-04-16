import os
import time

from app import create_app


def _make_client():
    os.environ["AUTO_OFF_SECONDS"] = "1"
    os.environ["DEFAULT_MODE"] = "auto"
    os.environ["MANUAL_OVERRIDE_SECONDS"] = "2"
    app = create_app()
    return app.test_client()


def test_bridge_motion_turns_light_on():
    client = _make_client()
    response = client.post("/bridge/motion-event", json={"detected": True})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["data"]["power"] == "on"
    assert payload["data"]["control_source"] == "motion"


def test_auto_off_after_no_motion_timeout():
    client = _make_client()
    client.post("/bridge/motion-event", json={"detected": True})
    time.sleep(1.2)
    status_response = client.get("/light/status")
    status_payload = status_response.get_json()
    assert status_payload["data"]["power"] == "off"
    assert status_payload["data"]["mode"] == "auto"
