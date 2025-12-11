"""Configuration settings for JARVIS 3.0"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
try:
    load_dotenv()
except ImportError:
    pass

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

# Flask Configuration
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

# Desktop App Configuration
DESKTOP_APP_TITLE = "Jarvis 3.0 - multimodel Assistant"
DESKTOP_APP_GEOMETRY = "1200x800"
DESKTOP_BG_COLOR = '#0a0a1a'

# MediaPipe Configuration
MEDIAPIPE_MIN_DETECTION_CONFIDENCE = 0.7
MEDIAPIPE_MIN_TRACKING_CONFIDENCE = 0.5

# Voice Recognition Configuration
VOICE_TIMEOUT = 5
VOICE_PHRASE_TIME_LIMIT = None

# Gesture Configuration
GESTURE_COOLDOWN = 20


