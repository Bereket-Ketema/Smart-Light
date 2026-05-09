from flask import Blueprint, request
from app.services.light_service import get_light_status, turn_light_off, turn_light_on
from app.utils.response import success_response

light_bp = Blueprint("light", __name__, url_prefix="/light")

@light_bp.get("/status")
def light_status():
    print("🔵 [LIGHT] GET /light/status - Request received")
    result = get_light_status()
    print(f"🟢 [LIGHT] Response: power={result.get('power')}, mode={result.get('mode')}")
    return success_response("Light status fetched", result)

@light_bp.post("/on")
def light_on():
    print("🔵 [LIGHT] POST /light/on - Request received")
    print(f"📥 Headers: {dict(request.headers)}")
    result = turn_light_on()
    print(f"🟢 [LIGHT] Response: power={result.get('power')}, mode={result.get('mode')}, override_until={result.get('override_until')}")
    return success_response("Light turned on manually", result)

@light_bp.post("/off")
def light_off():
    print("🔵 [LIGHT] POST /light/off - Request received")
    result = turn_light_off()
    print(f"🟢 [LIGHT] Response: power={result.get('power')}, mode={result.get('mode')}")
    return success_response("Light turned off manually", result)