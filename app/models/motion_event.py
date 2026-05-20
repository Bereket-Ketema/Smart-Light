# app/models/motion_event.py

from datetime import datetime, timezone
from typing import Optional

class MotionEvent:
    def __init__(self, detected: bool, timestamp: Optional[str] = None):
        self.detected = detected
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()
    
    @classmethod
    def from_payload(cls, payload: dict):
        detected = payload.get("detected", False)
        if isinstance(detected, str):
            detected = detected.lower() in ["true", "1", "yes"]
        if detected is not True:
            raise ValueError("`detected` must be true")
        timestamp = payload.get("timestamp")
        return cls(detected=detected, timestamp=timestamp)
