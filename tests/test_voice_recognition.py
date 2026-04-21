"""
Tests for voice recognition service
"""

import pytest
from unittest.mock import Mock, patch
from app.services.voice_recognition_service import VoiceRecognitionService


class TestVoiceRecognitionService:
    
    def test_parse_command_light_on(self):
        service = VoiceRecognitionService()
        result = service.parse_command("light on")
        assert result["success"] is True
        assert result["action"] == "LIGHT_ON"
    
    def test_parse_command_light_off(self):
        service = VoiceRecognitionService()
        result = service.parse_command("turn off the light")
        assert result["success"] is True
        assert result["action"] == "LIGHT_OFF"
    
    def test_parse_command_auto_mode(self):
        service = VoiceRecognitionService()
        result = service.parse_command("auto mode")
        assert result["success"] is True
        assert result["action"] == "AUTO_MODE"
    
    def test_parse_command_unknown(self):
        service = VoiceRecognitionService()
        result = service.parse_command("pizza")
        assert result["success"] is False
        assert "Unknown command" in result["message"]
    
    def test_parse_command_empty(self):
        service = VoiceRecognitionService()
        result = service.parse_command("")
        assert result["success"] is False
    
    @patch('speech_recognition.Recognizer')
    def test_listen_for_command_success(self, mock_recognizer_class):
        # This test would need microphone mocking
        # Simplified for now
        pass