from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass
class MotionEvent:
    detected: bool
    timestamp: str

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "MotionEvent":
        detected = payload.get("detected")
        if not isinstance(detected, bool):
            raise ValueError("`detected` must be a boolean value")
        if not detected:
            raise ValueError("only detected=true events are supported")

        timestamp = payload.get("timestamp")
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat()
        if not isinstance(timestamp, str):
            raise ValueError("`timestamp` must be a string when provided")

        return cls(detected=detected, timestamp=timestamp)
