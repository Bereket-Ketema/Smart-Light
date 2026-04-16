import os

from app import create_app


def _make_client():
    os.environ["AUTO_OFF_SECONDS"] = "1"
    os.environ["DEFAULT_MODE"] = "auto"
    os.environ["MANUAL_OVERRIDE_SECONDS"] = "2"
    app = create_app()
    return app.test_client()


def test_voice_light_off_overrides_motion():
    client = _make_client()
    client.post("/bridge/motion-event", json={"detected": True})

    voice_response = client.post("/voice/command", json={"command": "light off"})
    assert voice_response.status_code == 200
    voice_payload = voice_response.get_json()
    assert voice_payload["data"]["state"]["power"] == "off"
    assert voice_payload["data"]["state"]["mode"] == "manual"


def test_voice_auto_mode_reenables_automation():
    client = _make_client()
    client.post("/voice/command", json={"command": "light on"})

    auto_response = client.post("/voice/command", json={"command": "auto mode"})
    assert auto_response.status_code == 200
    auto_payload = auto_response.get_json()
    assert auto_payload["data"]["state"]["mode"] == "auto"
