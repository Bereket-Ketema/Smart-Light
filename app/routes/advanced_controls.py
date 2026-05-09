# app/routes/advanced_controls.py

from flask import Blueprint, request
from app.services.automation_service import set_auto_off_seconds
from app.state_store import update_state, get_state
from app.utils.response import error_response, success_response

advanced_controls_bp = Blueprint("advanced_controls", __name__)

_ALLOWED_SENSITIVITY = {"low", "medium", "high"}
_MIN_TIMER_SECONDS = 1

def _parse_json() -> dict:
    payload = request.get_json(silent=True)
    return payload if isinstance(payload, dict) else {}

@advanced_controls_bp.post("/brightness")
def set_brightness():
    print("🔵 [ADVANCED] POST /brightness - Request received")
    payload = _parse_json()
    print(f"📥 Payload: {payload}")
    
    brightness = payload.get("brightness")

    if not isinstance(brightness, int):
        return error_response("Invalid brightness", 422, {"detail": "`brightness` must be an integer"})
    if brightness < 0 or brightness > 100:
        return error_response("Invalid brightness", 422, {"detail": "`brightness` must be between 0 and 100"})

    updated = update_state(brightness=brightness, control_source="manual")
    print(f"🟢 [ADVANCED] Brightness set to {updated['brightness']}%")
    return success_response(
        "Brightness updated",
        {"status": "success", "brightness": updated["brightness"]},
    )

@advanced_controls_bp.get("/brightness")
def get_brightness():
    print("🔵 [ADVANCED] GET /brightness - Request received")
    state = get_state()
    print(f"🟢 [ADVANCED] Current brightness: {state.get('brightness', 70)}%")
    return success_response(
        "Brightness retrieved",
        {"brightness": state.get("brightness", 70)},
    )

@advanced_controls_bp.post("/sensitivity")
def set_sensitivity():
    print("🔵 [ADVANCED] POST /sensitivity - Request received")
    payload = _parse_json()
    print(f"📥 Payload: {payload}")
    
    sensitivity = payload.get("sensitivity")

    if not isinstance(sensitivity, str):
        return error_response("Invalid sensitivity", 422, {"detail": "`sensitivity` must be a string"})

    normalized = sensitivity.strip().lower()
    if normalized not in _ALLOWED_SENSITIVITY:
        return error_response(
            "Invalid sensitivity",
            422,
            {"detail": "`sensitivity` must be one of: low, medium, high"},
        )

    updated = update_state(sensitivity=normalized, control_source="manual")
    print(f"🟢 [ADVANCED] Sensitivity set to {updated['sensitivity']}")
    return success_response(
        "Sensitivity updated",
        {"status": "success", "sensitivity": updated["sensitivity"]},
    )

@advanced_controls_bp.get("/sensitivity")
def get_sensitivity():
    print("🔵 [ADVANCED] GET /sensitivity - Request received")
    state = get_state()
    print(f"🟢 [ADVANCED] Current sensitivity: {state.get('sensitivity', 'medium')}")
    return success_response(
        "Sensitivity retrieved",
        {"sensitivity": state.get("sensitivity", "medium")},
    )

@advanced_controls_bp.post("/timer")
def set_timer():
    print("🔵 [ADVANCED] POST /timer - Request received")
    payload = _parse_json()
    print(f"📥 Payload: {payload}")
    
    timer = payload.get("timer")

    if not isinstance(timer, int):
        return error_response("Invalid timer", 422, {"detail": "`timer` must be an integer (seconds)"})
    if timer < _MIN_TIMER_SECONDS:
        return error_response(
            "Invalid timer",
            422,
            {"detail": f"`timer` must be >= {_MIN_TIMER_SECONDS} second(s)"},
        )

    set_auto_off_seconds(timer)
    updated = update_state(timer=timer, control_source="manual")
    print(f"🟢 [ADVANCED] Timer set to {updated['timer']} seconds")
    return success_response(
        "Auto-off timer updated",
        {"status": "success", "timer": updated["timer"]},
    )

@advanced_controls_bp.get("/timer")
def get_timer():
    print("🔵 [ADVANCED] GET /timer - Request received")
    state = get_state()
    print(f"🟢 [ADVANCED] Current timer: {state.get('timer', 10)} seconds")
    return success_response(
        "Timer retrieved",
        {"timer": state.get("timer", 10)},
    )