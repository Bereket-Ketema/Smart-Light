"""Shared in-memory state for the Smart Light app."""

from threading import Lock
from typing import Any

from app.models.light_state import LightState


_state_lock = Lock()
_state = LightState()


def init_state(default_mode: str = "auto", auto_off_seconds: int = 10) -> None:
    with _state_lock:
        _state.power = "off"
        _state.brightness = 0
        _state.mode = default_mode
        _state.sensitivity = "medium"
        _state.timer = auto_off_seconds
        _state.last_motion_at = None
        _state.override_until = None
        _state.control_source = "system"


def get_state() -> dict[str, Any]:
    with _state_lock:
        return _state.to_dict()


def update_state(**kwargs: Any) -> dict[str, Any]:
    with _state_lock:
        for key, value in kwargs.items():
            if hasattr(_state, key):
                setattr(_state, key, value)
        return _state.to_dict()
