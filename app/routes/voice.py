from flask import Blueprint, request
from app.services.voice_service import (
    get_voice_control_status,
    listen_and_process_voice_command,
    process_voice_payload,
    set_voice_control_active,
)
from app.utils.response import error_response, success_response

voice_bp = Blueprint("voice", __name__, url_prefix="/voice")


def _parse_json() -> dict:
    payload = request.get_json(silent=True)
    return payload if isinstance(payload, dict) else {}


@voice_bp.get("/status")
def voice_status():
    print("🔵 [VOICE] GET /voice/status - Request received")
    return success_response("Voice control status fetched", get_voice_control_status())


@voice_bp.post("/control")
def voice_control():
    print("🔵 [VOICE] POST /voice/control - Request received")
    payload = _parse_json()
    enabled = payload.get("enabled")

    if not isinstance(enabled, bool):
        return error_response("Invalid voice control payload", 422, {"detail": "`enabled` must be a boolean"})

    status = set_voice_control_active(enabled)
    message = "Voice control enabled" if enabled else "Voice control disabled"
    return success_response(message, status)

@voice_bp.post("/command")
def voice_command():
    print("🔵 [VOICE] POST /voice/command - Request received")
    payload = _parse_json()
    print(f"📥 Request Body: {payload}")
    
    command = payload.get("command")
    print(f"🎤 Command text: '{command}'")
    
    try:
        action, updated_state = process_voice_payload(payload)
        print(f"✅ [VOICE] Action executed: {action}")
        print(f"📤 Response state: power={updated_state.get('power')}, mode={updated_state.get('mode')}")
        return success_response(
            "Voice command executed",
            {"action": action, "state": updated_state},
        )
    except ValueError as exc:
        print(f"❌ [VOICE] Error: {exc}")
        return error_response("Invalid voice command", 422, {"detail": str(exc)})


@voice_bp.post("/listen")
def voice_listen():
    print("🔵 [VOICE] POST /voice/listen - Request received")

    try:
        action, updated_state, command_text = listen_and_process_voice_command()
        return success_response(
            "Voice command listened and executed",
            {"action": action, "command": command_text, "state": updated_state},
        )
    except RuntimeError as exc:
        print(f"❌ [VOICE] Listen unavailable: {exc}")
        return error_response("Voice listening unavailable", 409, {"detail": str(exc)})
    except ValueError as exc:
        print(f"❌ [VOICE] Listen error: {exc}")
        return error_response("Invalid voice command", 422, {"detail": str(exc)})
