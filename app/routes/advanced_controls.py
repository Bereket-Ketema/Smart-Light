from flask import Blueprint, request

from app.services.automation_service import set_auto_off_seconds
from app.state_store import update_state
from app.utils.response import error_response, success_response


advanced_controls_bp = Blueprint("advanced_controls", __name__)

_ALLOWED_SENSITIVITY = {"low", "medium", "high"}
_MIN_TIMER_SECONDS = 1


def _parse_json() -> dict:
    payload = request.get_json(silent=True)
    return payload if isinstance(payload, dict) else {}


@advanced_controls_bp.post("/brightness")
def set_brightness():
    payload = _parse_json()
    brightness = payload.get("brightness")

    if not isinstance(brightness, int):
        return error_response("Invalid brightness", 422, {"detail": "`brightness` must be an integer"})
    if brightness < 0 or brightness > 100:
        return error_response("Invalid brightness", 422, {"detail": "`brightness` must be between 0 and 100"})

    updated = update_state(brightness=brightness, control_source="manual")
    return success_response(
        "Brightness updated",
        {"status": "success", "brightness": updated["brightness"]},
    )


@advanced_controls_bp.post("/sensitivity")
def set_sensitivity():
    payload = _parse_json()
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
    return success_response(
        "Sensitivity updated",
        {"status": "success", "sensitivity": updated["sensitivity"]},
    )


@advanced_controls_bp.post("/timer")
def set_timer():
    payload = _parse_json()
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
    return success_response(
        "Auto-off timer updated",
        {"status": "success", "timer": updated["timer"]},
    )
