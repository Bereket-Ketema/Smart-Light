from app.services.automation_service import process_voice_command


def process_voice_payload(payload: dict) -> tuple[str, dict]:
    command = payload.get("command")
    if not isinstance(command, str) or not command.strip():
        raise ValueError("`command` must be a non-empty string")
    return process_voice_command(command)
