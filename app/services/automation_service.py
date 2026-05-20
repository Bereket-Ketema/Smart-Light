# app/services/automation_service.py

from datetime import datetime, timedelta, timezone
import random
from app.models.command import VoiceCommand
from app.models.motion_event import MotionEvent
from app.state_store import get_state, update_state
from app.utils.scheduler import cancel, schedule

_AUTO_OFF_TIMER_KEY = "auto_off"
_MANUAL_OVERRIDE_TIMER_KEY = "manual_override"
_auto_off_seconds = 10
_manual_override_seconds = 30


def configure(auto_off_seconds: int, manual_override_seconds: int) -> None:
    global _auto_off_seconds, _manual_override_seconds
    _auto_off_seconds = auto_off_seconds
    _manual_override_seconds = manual_override_seconds
    print(f"🟡 [AUTO] Configured: auto_off={auto_off_seconds}s, manual_override={manual_override_seconds}s")
    cancel(_AUTO_OFF_TIMER_KEY)
    cancel(_MANUAL_OVERRIDE_TIMER_KEY)


def set_auto_off_seconds(auto_off_seconds: int) -> None:
    global _auto_off_seconds
    _auto_off_seconds = auto_off_seconds
    print(f"🟡 [AUTO] Auto-off timer set to {auto_off_seconds} seconds")
    cancel(_AUTO_OFF_TIMER_KEY)
    
    # Also update state
    update_state(timer=auto_off_seconds)
    
    state = get_state()
    if state["mode"] == "auto" and state["power"] == "on":
        _schedule_auto_off()


def get_auto_off_seconds() -> int:
    return _auto_off_seconds


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _schedule_auto_off() -> None:
    print(f"🟡 [AUTO] Scheduling auto-off in {_auto_off_seconds} seconds")
    schedule(_AUTO_OFF_TIMER_KEY, _auto_off_seconds, _auto_turn_off_if_needed)


def _schedule_manual_override_expiry() -> None:
    print(f"🟡 [AUTO] Scheduling manual override expiry in {_manual_override_seconds} seconds")
    schedule(
        _MANUAL_OVERRIDE_TIMER_KEY,
        _manual_override_seconds,
        _expire_manual_override_if_needed,
    )


def _auto_turn_off_if_needed() -> None:
    print("🟡 [AUTO] Auto-off timer triggered")
    state = get_state()
    if state["mode"] != "auto":
        print(f"🟡 [AUTO] Mode is {state['mode']}, not turning off")
        return
    if state["power"] == "off":
        print("🟡 [AUTO] Power already off")
        return
    print("🟢 [AUTO] Turning light off due to inactivity")
    update_state(power="off", control_source="auto_timeout")


def _expire_manual_override_if_needed() -> None:
    print("🟡 [AUTO] Manual override expiry triggered")
    state = get_state()
    if state["mode"] != "manual":
        print(f"🟡 [AUTO] Mode is {state['mode']}, not switching")
        return
    # ✅ FIX: Keep manual mode until user explicitly switches to auto
    # Do NOT automatically revert to auto mode
    print("🟡 [AUTO] Manual override expired, but keeping manual mode (user must explicitly switch)")
    update_state(override_until=None, control_source="manual_timeout")
    # Do NOT schedule auto-off - light should stay in its current state


def _should_detect_motion(sensitivity: str) -> bool:
    """Determine if motion should be detected based on sensitivity setting"""
    probabilities = {
        "low": 0.3,      # 30% chance
        "medium": 0.6,   # 60% chance
        "high": 0.9,     # 90% chance
    }
    probability = probabilities.get(sensitivity, 0.6)
    detected = random.random() < probability
    print(f"🟡 [AUTO] Sensitivity={sensitivity}, detection probability={probability}, result={detected}")
    return detected


def handle_motion_event(event: MotionEvent) -> dict:
    print(f"🟡 [AUTO] handle_motion_event called")
    print(f"   - Timestamp: {event.timestamp}")
    print(f"   - Detected: {event.detected}")
    
    state = get_state()
    updated = update_state(last_motion_at=event.timestamp)

    if state["mode"] != "auto":
        print(f"🟡 [AUTO] Mode is {state['mode']}, ignoring motion (auto mode required)")
        return updated
    
    # Check sensitivity
    sensitivity = state.get("sensitivity", "medium")
    if not _should_detect_motion(sensitivity):
        print(f"🟡 [AUTO] Motion ignored due to sensitivity setting ({sensitivity})")
        return updated
    
    if not event.detected:
        print("🟡 [AUTO] Motion event: detected=False, ignoring")
        return updated
    
    print("🟢 [AUTO] Motion detected! Turning light ON and scheduling auto-off")
    updated = update_state(power="on", control_source="motion")
    _schedule_auto_off()
    return updated


def set_manual_power(power: str) -> dict:
    print(f"🟡 [AUTO] set_manual_power called with power='{power}'")
    override_until = (datetime.now(timezone.utc) + timedelta(seconds=_manual_override_seconds)).isoformat()
    cancel(_AUTO_OFF_TIMER_KEY)
    updated = update_state(
        power=power,
        mode="manual",
        override_until=override_until,
        control_source="manual",
    )
    _schedule_manual_override_expiry()
    print(f"🟢 [AUTO] set_manual_power result: power={updated['power']}, mode={updated['mode']}")
    return updated


def set_auto_mode() -> dict:
    print("🟡 [AUTO] set_auto_mode called")
    cancel(_MANUAL_OVERRIDE_TIMER_KEY)
    updated = update_state(mode="auto", override_until=None, control_source="voice")
    print(f"🟢 [AUTO] set_auto_mode result: mode={updated['mode']}, power={updated['power']}")
    if updated["power"] == "on":
        print("🟡 [AUTO] Power is on, scheduling auto-off")
        _schedule_auto_off()
    return updated


def process_voice_command(command_text: str) -> tuple[str, dict]:
    print(f"🟡 [AUTO] process_voice_command called with: '{command_text}'")
    parsed = VoiceCommand.from_text(command_text)
    print(f"   - Parsed action: {parsed.action}")
    
    if parsed.action == "LIGHT_ON":
        return parsed.action, set_manual_power("on")
    if parsed.action == "LIGHT_OFF":
        return parsed.action, set_manual_power("off")
    if parsed.action == "AUTO_MODE":
        return parsed.action, set_auto_mode()
    raise ValueError(f"unsupported voice command: {command_text}")