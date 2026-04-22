from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class LightState:
    power: str = "off"
    brightness: int = 0
    mode: str = "auto"
    sensitivity: str = "medium"
    timer: int = 10
    last_motion_at: Optional[str] = None
    override_until: Optional[str] = None
    control_source: str = "system"

    def to_dict(self) -> dict:
        return asdict(self)
