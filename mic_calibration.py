"""
Adaptive Microphone Calibration System for ILLI.
Measures ambient noise and adjusts speech recognition sensitivity.
"""
import logging
import speech_recognition as sr
from illi.memory.memory_system import LocalMemorySystem # Assuming this is the new path

logger = logging.getLogger(__name__)

class AdaptiveMicrophoneCalibration:
    """
    Adaptive microphone calibration system.
    Measures ambient noise and adjusts speech recognition sensitivity.
    """
    
    def __init__(self):
        self.memory_system = LocalMemorySystem()
        self.calibration_level = 0.0
        self.is_calibrating = False
    
    def run_ambient_noise_check(self, duration_seconds: int = 3) -> float:
        """
        Perform room acoustic noise baseline measurement.
        Returns ambient noise level (0-100 scale).
        """
        try:
            self.is_calibrating = True
            recognizer = sr.Recognizer()
            
            with sr.Microphone() as source:
                logger.info(f"Starting {duration_seconds}s ambient noise calibration...")
                recognizer.adjust_for_ambient_noise(source, duration=duration_seconds)
                
                # Estimate noise level
                noise_level = recognizer.energy_threshold
                # Map to a 0-100 scale for easier interpretation, adjust divisor as needed
                self.calibration_level = min(100, (noise_level / 4000) * 100) 
            
            self.memory_system.store_mic_calibration(self.calibration_level, "standard_room")
            self.is_calibrating = False
            
            logger.info(f"Mic calibration complete: {self.calibration_level:.1f}")
            return self.calibration_level
        
        except ImportError:
            logger.warning("speech_recognition not available; calibration skipped")
            return 0.0
        except Exception as e:
            logger.error(f"Calibration failed: {str(e)}")
            self.is_calibrating = False
            return 0.0
    
    def get_calibration_sensitivity(self) -> float:
        """Get current microphone sensitivity threshold."""
        stored = self.memory_system.get_latest_mic_calibration()
        if stored:
            self.calibration_level = stored
        return self.calibration_level
    
    def apply_calibration_to_recognizer(self, recognizer: sr.Recognizer) -> bool:
        """Apply calibration settings to speech recognizer."""
        try:
            calibration = self.get_calibration_sensitivity()
            # Map calibration level back to energy threshold
            recognizer.energy_threshold = (calibration / 100) * 4000
            logger.info(f"Applied calibration: threshold={recognizer.energy_threshold:.0f}")
            return True
        except Exception as e:
            logger.error(f"Failed to apply calibration: {str(e)}")
            return False