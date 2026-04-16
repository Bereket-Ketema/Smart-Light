from app.models.motion_event import MotionEvent
from app.services.automation_service import handle_motion_event


def process_motion_payload(payload: dict) -> dict:
    event = MotionEvent.from_payload(payload)
    return handle_motion_event(event)
