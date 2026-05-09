from flask import Blueprint
from app.state_store import get_state
from app.utils.response import success_response

debug_bp = Blueprint("debug", __name__, url_prefix="/debug")

@debug_bp.get("/state")
def get_full_state():
    """View the current full state of the system"""
    state = get_state()
    print("🔍 [DEBUG] Full state requested")
    return success_response("Current system state", state)