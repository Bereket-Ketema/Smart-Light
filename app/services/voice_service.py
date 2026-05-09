from app.services.automation_service import process_voice_command


def process_voice_payload(payload: dict) -> tuple[str, dict]:
    command = payload.get("command")
    print(f"🟡 [VOICE_SERVICE] Processing payload: {payload}")
    print(f"🎤 Command text: '{command}'")
    
    if not isinstance(command, str) or not command.strip():
        print("❌ [VOICE_SERVICE] Invalid command - empty or not a string")
        raise ValueError("`command` must be a non-empty string")
    
    print(f"🟡 [VOICE_SERVICE] Calling process_voice_command with '{command}'")
    return process_voice_command(command)