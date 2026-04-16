from flask import Blueprint, request

from app.services.motion_service import process_motion_payload
from app.utils.response import error_response, success_response


motion_bp = Blueprint("motion", __name__, url_prefix="/motion")


@motion_bp.post("/simulate")
def simulate_motion():
    payload = request.get_json(silent=True) or {"detected": True}
    try:
        updated_state = process_motion_payload(payload)
    except ValueError as exc:
        return error_response("Invalid motion payload", 422, {"detail": str(exc)})
    return success_response("Motion processed", updated_state)
