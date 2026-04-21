from flask import Blueprint, request

from app.services.voice_service import process_voice_payload
from app.services.automation_service import process_voice_command
from app.services.voice_recognition_service import get_voice_service
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


@voice_bp.post("/listen")
def voice_listen():
   
    voice_service = get_voice_service()
    
    
    if not voice_service.is_available():
        return error_response(
            "Voice service unavailable - no microphone detected",
            503,
            {"error_code": "MICROPHONE_NOT_FOUND"}
        )
    
    
    action, result = voice_service.process_voice_command()
    
    if action is None:
        return error_response(
            result.get("message", "Voice recognition failed"),
            400,
            {"error_code": "RECOGNITION_FAILED", "details": result}
        )
    
    
    try:
        
        command_text = action.lower().replace("_", " ")
        executed_action, updated_state = process_voice_command(command_text)
        return success_response(
            "Voice command executed successfully",
            {
                "action": executed_action,
                "recognized_command": result.get("command_text"),
                "state": updated_state
            }
        )
    except ValueError as exc:
        return error_response(
            f"Command '{action}' is not supported",
            422,
            {"detail": str(exc)}
        )


@voice_bp.get("/status")
def voice_status():
    
    voice_service = get_voice_service()
    return success_response(
        "Voice service status",
        {
            "available": voice_service.is_available(),
            "microphone_detected": voice_service.microphone_index is not None
        }
    )