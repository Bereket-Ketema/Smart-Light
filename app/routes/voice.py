from flask import Blueprint, request
from app.services.voice_service import process_voice_payload
from app.utils.response import error_response, success_response

voice_bp = Blueprint("voice", __name__, url_prefix="/voice")

@voice_bp.post("/command")
def voice_command():
    print("🔵 [VOICE] POST /voice/command - Request received")
    payload = request.get_json(silent=True) or {}
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