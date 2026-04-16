from flask import Blueprint, request

from app.services.voice_service import process_voice_payload
from app.utils.response import error_response, success_response


voice_bp = Blueprint("voice", __name__, url_prefix="/voice")


@voice_bp.post("/command")
def voice_command():
    payload = request.get_json(silent=True) or {}
    try:
        action, updated_state = process_voice_payload(payload)
    except ValueError as exc:
        return error_response("Invalid voice command", 422, {"detail": str(exc)})

    return success_response(
        "Voice command executed",
        {"action": action, "state": updated_state},
    )
