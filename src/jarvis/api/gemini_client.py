"""Gemini AI Client Module"""
import google.generativeai as genai
from jarvis.config.settings import GEMINI_API_KEY, GEMINI_MODEL

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
else:
    model = None


def process_prompt(prompt):
    """
    Process a prompt using Gemini AI
    
    Args:
        prompt (str): The user's prompt/question
        
    Returns:
        str: The AI's response or error message
    """
    if not GEMINI_API_KEY:
        return "Error: API key not configured. Please set GEMINI_API_KEY environment variable."
    
    if not model:
        return "Error: Gemini model not initialized. Please check your API key."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"


def is_api_configured():
    """Check if API is properly configured"""
    return bool(GEMINI_API_KEY and model)


