"""Voice Control Module"""
import speech_recognition as sr
import pyttsx3
import threading
import time
from jarvis.config.settings import VOICE_TIMEOUT, VOICE_PHRASE_TIME_LIMIT


class VoiceController:
    """Handles voice recognition and text-to-speech"""
    
    def __init__(self):
        self.voice_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
            self.microphone_available = True
        except (AttributeError, OSError) as e:
            print(f"Warning: Microphone not available: {e}")
            self.microphone = None
            self.microphone_available = False
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        if not self.microphone_available or self.microphone is None:
            return False, "Microphone not available"
        
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            return True, "Microphone calibrated successfully"
        except Exception as e:
            return False, f"Microphone calibration failed: {str(e)}"
    
    def listen_for_command(self, timeout=VOICE_TIMEOUT):
        """Listen for a voice command"""
        if not self.microphone_available or self.microphone is None:
            return None, "Microphone not available"
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=VOICE_PHRASE_TIME_LIMIT
                )
                command = self.recognizer.recognize_google(audio)
                return command.lower(), None
        except sr.WaitTimeoutError:
            return None, "No speech detected"
        except sr.UnknownValueError:
            return None, "Could not understand the audio"
        except sr.RequestError as e:
            return None, f"Could not request results: {e}"
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def speak_text(self, text):
        """Speak the given text"""
        try:
            self.voice_engine.say(text)
            self.voice_engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error speaking text: {str(e)}")
            return False


