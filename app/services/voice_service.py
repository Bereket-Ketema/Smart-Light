from app.services.automation_service import process_voice_command
from app.services.voice_recognition_service import get_voice_service

_voice_control_active = False


def set_voice_control_active(active: bool) -> dict:
    global _voice_control_active
    _voice_control_active = active
    return get_voice_control_status()


def get_voice_control_status() -> dict:
    voice_service = get_voice_service()
    return {
        "active": _voice_control_active,
        "server_listen_available": voice_service.is_available(),
        "server_listen_dependency_installed": voice_service.dependency_installed,
        "server_listen_unavailable_reason": voice_service.unavailable_reason,
    }


def process_voice_payload(payload: dict) -> tuple[str, dict]:
    command = payload.get("command")
    print(f"🟡 [VOICE_SERVICE] Processing payload: {payload}")
    print(f"🎤 Command text: '{command}'")
    
    if not isinstance(command, str) or not command.strip():
        print("❌ [VOICE_SERVICE] Invalid command - empty or not a string")
        raise ValueError("`command` must be a non-empty string")
    
    print(f"🟡 [VOICE_SERVICE] Calling process_voice_command with '{command}'")
    return process_voice_command(command)


def listen_and_process_voice_command() -> tuple[str, dict, str]:
    if not _voice_control_active:
        raise RuntimeError("Voice control is not active")

    voice_service = get_voice_service()
    if not voice_service.is_available():
        reason = voice_service.unavailable_reason or "Server microphone is not available"
        raise RuntimeError(reason)

    action, result = voice_service.process_voice_command()
    if not action or not result or not result.get("success"):
        message = result.get("message") if isinstance(result, dict) else "No voice command detected"
        raise ValueError(message)

    command_text = result.get("command_text")
    if not isinstance(command_text, str) or not command_text.strip():
        raise ValueError("No command text recognized")

    executed_action, updated_state = process_voice_command(command_text)
    return executed_action, updated_state, command_text
