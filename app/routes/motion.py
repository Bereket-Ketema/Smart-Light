from flask import Blueprint, request
from app.services.motion_service import process_motion_payload
from app.utils.response import error_response, success_response

motion_bp = Blueprint("motion", __name__, url_prefix="/motion")

@motion_bp.post("/simulate")
def simulate_motion():
    print("🔵 [MOTION] POST /motion/simulate - Request received")
    payload = request.get_json(silent=True) or {"detected": True}
    print(f"📥 Payload: {payload}")
    
    try:
        updated_state = process_motion_payload(payload)
        print(f"🟢 [MOTION] Processed - power={updated_state.get('power')}, mode={updated_state.get('mode')}")
        return success_response("Motion processed", updated_state)
    except ValueError as exc:
        print(f"❌ [MOTION] Error: {exc}")
        return error_response("Invalid motion payload", 422, {"detail": str(exc)})