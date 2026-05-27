import speech_recognition as sr
import threading
import time


def calibrate(duration: float = 1.5):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=duration)
            return {'energy_threshold': r.energy_threshold}
    except Exception as e:
        raise


def listen(threshold: int = None, timeout: int = 6):
    r = sr.Recognizer()
    if threshold:
        r.energy_threshold = threshold
    with sr.Microphone() as src:
        r.adjust_for_ambient_noise(src, duration=0.8)
        audio = r.listen(src, timeout=timeout, phrase_time_limit=timeout)
        try:
            text = r.recognize_sphinx(audio)
            return text
        except Exception:
            try:
                # fallback to google if available (requires internet)
                return r.recognize_google(audio)
            except Exception as e:
                raise

