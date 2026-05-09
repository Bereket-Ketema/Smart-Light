# app/state_store.py

from datetime import datetime, timezone
from typing import Any, Dict, Optional

_state: Dict[str, Any] = {}

def init_state(default_mode: str = "auto", auto_off_seconds: int = 10) -> None:
    """Initialize the global state"""
    global _state
    _state = {
        "power": "off",
        "mode": default_mode,
        "brightness": 70,
        "sensitivity": "medium",
        "timer": auto_off_seconds,
        "last_motion_at": None,
        "override_until": None,
        "control_source": "init",
    }
    print(f"🟢 [STATE] Initialized: power=off, mode={default_mode}, brightness=70, sensitivity=medium, timer={auto_off_seconds}")

def get_state() -> Dict[str, Any]:
    """Get current state"""
    return _state.copy()

def update_state(**kwargs) -> Dict[str, Any]:
    """Update state with given key-value pairs"""
    global _state
    _state.update(kwargs)
    
    # Log significant changes
    if "power" in kwargs:
        print(f"🟡 [STATE] Power changed to: {kwargs['power']}")
    if "mode" in kwargs:
        print(f"🟡 [STATE] Mode changed to: {kwargs['mode']}")
    if "brightness" in kwargs:
        print(f"🟡 [STATE] Brightness changed to: {kwargs['brightness']}%")
    if "sensitivity" in kwargs:
        print(f"🟡 [STATE] Sensitivity changed to: {kwargs['sensitivity']}")
    if "timer" in kwargs:
        print(f"🟡 [STATE] Timer changed to: {kwargs['timer']} seconds")
    
    return _state.copy()