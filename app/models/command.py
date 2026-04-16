from dataclasses import dataclass


@dataclass
class VoiceCommand:
    raw: str
    normalized: str
    action: str

    @classmethod
    def from_text(cls, command_text: str) -> "VoiceCommand":
        normalized = " ".join(command_text.lower().strip().split())

        command_to_action = {
            "light on": "LIGHT_ON",
            "turn on light": "LIGHT_ON",
            "light off": "LIGHT_OFF",
            "turn off light": "LIGHT_OFF",
            "auto mode": "AUTO_MODE",
        }
        action = command_to_action.get(normalized, "UNKNOWN")
        return cls(raw=command_text, normalized=normalized, action=action)
