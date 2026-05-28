"""
ILLI Multi-Voice Synthesis Engine: Dual-voice (Male/Female) offline TTS.
Uses local pyttsx3 for text-to-speech without cloud APIs.
"""
import logging
import pyttsx3
from pathlib import Path
from typing import Optional, Dict, List
from illi.memory.memory_system import LocalMemorySystem # Assuming this is the new path

logger = logging.getLogger(__name__)

class MultiVoiceSynthesisEngine:
    """
    Multi-voice synthesis engine for Male/Female offline voices.
    Uses local pyttsx3 for text-to-speech without cloud APIs.
    """
    
    def __init__(self):
        self.engine = None
        self.available_voices = []
        self.current_voice_gender = "male" # Default
        self.memory_system = LocalMemorySystem()
        
        self._initialize_tts_engine()
    
    def _initialize_tts_engine(self):
        """Initialize pyttsx3 text-to-speech engine."""
        try:
            self.engine = pyttsx3.init()
            
            # Discover available voices
            voices = self.engine.getProperty('voices')
            self.available_voices = [
                {
                    "id": voice.id,
                    "name": voice.name,
                    "gender": "male" if "male" in voice.name.lower() else "female",
                }
                for voice in voices
            ]
            
            # Attempt to set a default voice based on preference or first available
            preferred_gender = self.memory_system.get_preference("active_voice_gender", "male")
            self.select_voice(preferred_gender)

            logger.info(f"TTS Engine initialized with {len(self.available_voices)} voices.")
            logger.debug(f"Available voices: {[v['name'] for v in self.available_voices]}")
        except ImportError:
            logger.warning("pyttsx3 not available; text-to-speech disabled.")
            self.engine = None
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None
    
    def list_available_voices(self) -> List[Dict]:
        """List all available voice profiles."""
        return self.available_voices
    
    def select_voice(self, voice_gender: str = "male") -> bool:
        """Select voice type (male/female)."""
        if not self.engine:
            logger.error("TTS engine not available.")
            return False
        
        target_voice = next(
            (v for v in self.available_voices if v["gender"] == voice_gender.lower()),
            None
        )
        
        if target_voice:
            self.engine.setProperty('voice', target_voice["id"])
            self.current_voice_gender = voice_gender
            self.memory_system.set_preference("active_voice_gender", voice_gender)
            logger.info(f"Voice switched to: {target_voice['name']} ({voice_gender}).")
            return True
        else:
            logger.error(f"Voice gender '{voice_gender}' not found.")
            return False
    
    def set_voice_parameters(self, rate: int = 150, volume: float = 1.0) -> bool:
        """Configure voice pitch, rate, and volume."""
        if not self.engine:
            return False
        try:
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            logger.info(f"Voice parameters set: rate={rate}, volume={volume}.")
            return True
        except Exception as e:
            logger.error(f"Failed to set voice parameters: {str(e)}")
            return False
    
    def speak(self, text: str, save_to_file: Optional[Path] = None) -> bool:
        """Convert text to speech."""
        if not self.engine:
            logger.error("TTS engine not available.")
            return False
        try:
            if save_to_file:
                self.engine.save_to_file(text, str(save_to_file))
            else:
                self.engine.say(text)
            self.engine.runAndWait()
            logger.info(f"Speech synthesized: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Speech synthesis failed: {str(e)}")
            return False
    
    def speak_adaptive(self, text: str):
        """Speak text, integrating user's preferred call name from memory."""
        user_name = self.memory_system.get_preference("user_call_name", "Sir")
        adaptive_text = text.replace("[USER_NAME]", user_name)
        return self.speak(adaptive_text)