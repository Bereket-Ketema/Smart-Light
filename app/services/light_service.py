from app.services.automation_service import set_manual_power
from app.state_store import get_state


def get_light_status() -> dict:
    return get_state()


def turn_light_on() -> dict:
    return set_manual_power("on", 100, "medium")


def turn_light_off() -> dict:
    return set_manual_power("off", 0, "medium")
