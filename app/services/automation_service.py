from datetime import datetime, timedelta, timezone

from app.models.command import VoiceCommand
from app.models.motion_event import MotionEvent
from app.state_store import get_state, update_state
from app.utils.scheduler import cancel, schedule


_AUTO_OFF_TIMER_KEY = "auto_off"
_auto_off_seconds = 10
_manual_override_seconds = 30


def configure(auto_off_seconds: int, manual_override_seconds: int) -> None:
    global _auto_off_seconds, _manual_override_seconds
    _auto_off_seconds = auto_off_seconds
    _manual_override_seconds = manual_override_seconds


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _schedule_auto_off() -> None:
    schedule(_AUTO_OFF_TIMER_KEY, _auto_off_seconds, _auto_turn_off_if_needed)


def _auto_turn_off_if_needed() -> None:
    state = get_state()
    if state["mode"] != "auto":
        return
    if state["power"] == "off":
        return
    update_state(power="off", control_source="auto_timeout")


def handle_motion_event(event: MotionEvent) -> dict:
    state = get_state()
    updated = update_state(last_motion_at=event.timestamp)

    if state["mode"] != "auto":
        return updated

    updated = update_state(power="on", control_source="motion")
    _schedule_auto_off()
    return updated


def set_manual_power(power: str) -> dict:
    override_until = (datetime.now(timezone.utc) + timedelta(seconds=_manual_override_seconds)).isoformat()
    cancel(_AUTO_OFF_TIMER_KEY)
    return update_state(
        power=power,
        mode="manual",
        override_until=override_until,
        control_source="manual",
    )


def set_auto_mode() -> dict:
    updated = update_state(mode="auto", override_until=None, control_source="voice")
    if updated["power"] == "on":
        _schedule_auto_off()
    return updated


def process_voice_command(command_text: str) -> tuple[str, dict]:
    parsed = VoiceCommand.from_text(command_text)
    if parsed.action == "LIGHT_ON":
        return parsed.action, set_manual_power("on")
    if parsed.action == "LIGHT_OFF":
        return parsed.action, set_manual_power("off")
    if parsed.action == "AUTO_MODE":
        return parsed.action, set_auto_mode()
    raise ValueError("unsupported voice command")
