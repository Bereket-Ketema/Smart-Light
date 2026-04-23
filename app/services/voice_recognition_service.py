import logging
from typing import Dict, Optional, Protocol, Tuple

try:
    import speech_recognition as spR
except ModuleNotFoundError:  # pragma: no cover
    spR = None

logger = logging.getLogger(__name__)


class VoiceService(Protocol):
    microphone_index: Optional[int]
    dependency_installed: bool
    unavailable_reason: Optional[str]

    def is_available(self) -> bool: ...
    def process_voice_command(self) -> Tuple[Optional[str], Optional[Dict]]: ...


class VoiceRecognitionService:
    dependency_installed = True
    
    def __init__(self):
        if spR is None:
            raise RuntimeError("speech_recognition is not installed")
        self.recognizer = spR.Recognizer()
        self.microphone_index = self._find_working_microphone()
        self.unavailable_reason = None if self.microphone_index is not None else "No microphone detected"
        
    def _find_working_microphone(self) -> Optional[int]:

        try:
            mics = spR.Microphone.list_microphone_names()
            logger.info(f"Found {len(mics)} microphone(s)")
            for i, name in enumerate(mics):
                logger.debug(f"   {i}: {name}")
            return 0  # Use default microphone
        except Exception as e:
            logger.error(f"Microphone error: {e}")
            return None
    
    def is_available(self) -> bool:

        return self.microphone_index is not None
    
    def listen_for_command(self, timeout: int = 5) -> Optional[str]:

        if not self.is_available():
            logger.error("No microphone available")
            return None
            
        try:
            with spR.Microphone(device_index=self.microphone_index) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=timeout)
                
                # Recognize using Google's free API
                command = self.recognizer.recognize_google(audio).lower()
                logger.info(f"Voice recognized: '{command}'")
                return command
                
        except spR.WaitTimeoutError:
            logger.warning("No speech detected within timeout")
            return None
        except spR.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except Exception as e:
            logger.error(f"Voice recognition error: {e}")
            return None
    
    def parse_command(self, command: str) -> Dict:

        if not command:
            return {"success": False, "message": "No command received"}
        
        command_lower = command.lower()
        
        # Map voice commands to actions
        if "light on" in command_lower or "turn on" in command_lower:
            return {"success": True, "action": "LIGHT_ON", "command_text": "light on"}
        elif "light off" in command_lower or "turn off" in command_lower:
            return {"success": True, "action": "LIGHT_OFF", "command_text": "light off"}
        elif "auto mode" in command_lower or "automatic" in command_lower:
            return {"success": True, "action": "AUTO_MODE", "command_text": "auto mode"}
        else:
            return {
                "success": False, 
                "message": f"Unknown command: '{command}'",
                "suggested": "Say 'light on', 'light off', or 'auto mode'"
            }
    
    def process_voice_command(self) -> Tuple[Optional[str], Optional[Dict]]:

        # Step 1: Listen
        command_text = self.listen_for_command()
        if not command_text:
            return None, {"success": False, "message": "No voice detected"}
        
        # Step 2: Parse
        parsed = self.parse_command(command_text)
        if not parsed["success"]:
            return None, parsed
        
        return parsed["action"], parsed

# Singleton instance
_voice_service: Optional[VoiceService] = None

class _UnavailableVoiceRecognitionService:
    dependency_installed = False
    microphone_index = None
    unavailable_reason = "Voice recognition dependency not installed"

    def is_available(self) -> bool:
        return False

    def process_voice_command(self) -> Tuple[Optional[str], Optional[Dict]]:
        return None, {"success": False, "message": "Voice recognition dependency not installed"}


def get_voice_service() -> VoiceService:

    global _voice_service
    if _voice_service is None:
        if spR is None:
            _voice_service = _UnavailableVoiceRecognitionService()
        else:
            _voice_service = VoiceRecognitionService()
    return _voice_service
