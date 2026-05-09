from flask import Blueprint, request
from app.services.motion_service import process_motion_payload
from app.utils.response import error_response, success_response

bridge_bp = Blueprint("bridge", __name__, url_prefix="/bridge")

@bridge_bp.post("/motion-event")
def bridge_motion_event():
    print("🔵 [BRIDGE] POST /bridge/motion-event - Request received")
    payload = request.get_json(silent=True) or {}
    print(f"📥 Payload: {payload}")
    
    try:
        updated_state = process_motion_payload(payload)
        print(f"🟢 [BRIDGE] Processed - power={updated_state.get('power')}, mode={updated_state.get('mode')}")
        return success_response("Bridge motion event processed", updated_state)
    except ValueError as exc:
        print(f"❌ [BRIDGE] Error: {exc}")
        return error_response("Invalid bridge motion payload", 422, {"detail": str(exc)})