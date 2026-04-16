from flask import Blueprint

from app.services.light_service import get_light_status, turn_light_off, turn_light_on
from app.utils.response import success_response


light_bp = Blueprint("light", __name__, url_prefix="/light")


@light_bp.get("/status")
def light_status():
    return success_response("Light status fetched", get_light_status())


@light_bp.post("/on")
def light_on():
    return success_response("Light turned on manually", turn_light_on())


@light_bp.post("/off")
def light_off():
    return success_response("Light turned off manually", turn_light_off())
