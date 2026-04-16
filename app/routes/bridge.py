from flask import Blueprint, request

from app.services.motion_service import process_motion_payload
from app.utils.response import error_response, success_response


bridge_bp = Blueprint("bridge", __name__, url_prefix="/bridge")


@bridge_bp.post("/motion-event")
def bridge_motion_event():
    payload = request.get_json(silent=True) or {}
    try:
        updated_state = process_motion_payload(payload)
    except ValueError as exc:
        return error_response("Invalid bridge motion payload", 422, {"detail": str(exc)})

    return success_response("Bridge motion event processed", updated_state)
