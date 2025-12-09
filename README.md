# 🤖 Jarvis 3.0 – Multimodal AI Assistant

A modern, feature-rich web interface for JARVIS, powered by Google's Gemini AI.

## Features

✨ **Modern UI/UX**
- Beautiful, responsive design with dark/light theme toggle
- Smooth animations and transitions
- Mobile-friendly interface

💬 **Advanced Chat Features**
- Real-time messaging with typing indicators
- Message history persistence
- Quick suggestion chips
- Export conversations

🎨 **Customization**
- Theme switching (Dark/Light mode)
- Settings panel
- Customizable response settings

🚀 **Performance**
- Fast and responsive
- Optimized for all screen sizes
- Clean, maintainable code

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd JARVIS3.0
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Option 1: Environment variable (Recommended)
   ```bash
   # Windows
   set GEMINI_API_KEY=your_api_key_here
   
   # Linux/Mac
   export GEMINI_API_KEY=your_api_key_here
   ```
   
   Option 2: Create a `.env` file
   ```bash
   cp .env.example .env
   # Then edit .env and add your API key
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Getting Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and set it as described above

## Project Structure

```
JARVIS3.0/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css    # Styling
│   └── js/
│       └── app.js       # Frontend logic
└── README.md            # This file
```

## Usage

1. Start the server using `python app.py`
2. Open the web interface in your browser
3. Type your message and press Enter or click Send
4. Use suggestion chips for quick prompts
5. Access settings via the sidebar
6. Export conversations using the download button

## Features in Detail

### Chat Interface
- **Real-time messaging**: Instant responses from Gemini AI
- **Message history**: Automatically saved and restored
- **Typing indicators**: Visual feedback when AI is processing
- **Quick suggestions**: Pre-defined prompt chips for common tasks

### Customization
- **Theme toggle**: Switch between dark and light modes
- **Settings panel**: Configure API key and preferences
- **Export chat**: Download conversations as text files

### Responsive Design
- Works seamlessly on desktop, tablet, and mobile devices
- Collapsible sidebar for mobile
- Touch-friendly interface

## Troubleshooting

**API Key Issues**
- Make sure your API key is correctly set
- Check that the key has proper permissions
- Verify the key is active in Google AI Studio

**Port Already in Use**
- Change the port in `app.py`: `app.run(port=5001)`

**Module Not Found**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## Future Enhancements

- [ ] Voice input/output
- [ ] File upload and analysis
- [ ] Multi-language support
- [ ] Conversation search
- [ ] Custom AI model selection
- [ ] Plugin system

## License

This project is open source and available for personal use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

Made with ❤️ for AI enthusiasts




---

## 🚀 Features

- 🎙️ **Voice Control:**  
  Execute system commands and interact naturally using speech recognition.

  🔒 ***Lock/Unlock System using Voice:***

- ✋ **Gesture Recognition (via MediaPipe):**  
  Control applications, volume, and playback with hand movements.

- 📸 **Camera Feed Integration:**  
  Real-time camera processing with motion feedback.

- 🖥️ **GUI Interface:**  
  Built with **Tkinter**, providing live camera feed, console logs, and interactive control buttons.

- 💬 **Text-to-Speech (TTS):**  
  Responses and alerts via `pyttsx3`.

- 🧠 **Multithreading Support:**  
  Smooth execution of multiple tasks (voice + motion + camera).

  ----
  ## requirements.txt
  Flask==3.0.0
flask-cors==4.0.0
google-generativeai==0.3.2
python-dotenv==1.0.0

---

## 🧩 Tech Stack

- **Language:** Python 3.12  
- **Libraries Used:**
  - `opencv-python`
  - `numpy`
  - `pyttsx3`
  - `speechrecognition`
  - `pyautogui`
  - `pillow`
  - `screeninfo`
  - `keyboard`
  - `pyaudio`
  - `mediapipe` (for motion/gesture recognition)

---

## ⚙️ Installation

### 1️⃣ Prerequisites
Make sure you have **Python 3.12** installed.  
If not, you can install it from:  
👉 [https://www.python.org/downloads/release/python-3120/](https://www.python.org/downloads/release/python-3120/)

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/<tusharkantimahato>/Jarvis3.0.git
cd Jarvis3.0


3️⃣ Install Dependencies
py -3.12 -m pip install opencv-python numpy pyttsx3 speechrecognition pyautogui pillow screeninfo keyboard pyaudio --quiet

If you want motion control (hand gestures):
py -3.12 -m pip install mediapipe


⚠️ Note: mediapipe may not be available for Python 3.13.
Use Python 3.11 or 3.12 for full motion-control features.


🧠 Running the Project
py -3.12 main.py

Once launched, the GUI will appear with:


Buttons for Voice, Motion, and Camera Control


A console window for real-time Jarvis responses


Live camera feed for motion tracking



🗣️ Voice Commands
Some example commands:


“Start camera”


“Stop camera”


“Take picture”


“Volume up” / “Volume down”


“Open notepad”


“What is the time?”


“Hello Jarvis”



✋ Gesture Controls
GestureAction👍 Thumbs DownVolume Down✋ Open PalmPlay/Pause Media☝️ Pointing Up(Reserved for custom actions)

# JARVIS 3.0 - Project Structure

This document describes the organized file and folder structure of the JARVIS 3.0 project.

## 📁 Directory Structure
JARVIS3.0/
├── src/                          # Source code directory
│   ├── api/                      # API and Backend modules
│   │   ├── __init__.py
│   │   ├── gemini_client.py      # Gemini AI client wrapper
│   │   ├── routes.py             # Flask API routes
│   │   ├── cli.py                # Command-line interface
│   │   └── new_api.py            # Alternative API implementation
│   │
│   ├── desktop/                  # Desktop application (Tkinter)
│   │   ├── __init__.py
│   │   ├── app.py                # Main desktop application
│   │   ├── command_processor.py  # Command processing logic
│   │   │
│   │   ├── gui/                  # GUI components
│   │   │   ├── __init__.py
│   │   │   └── components.py    # Reusable GUI widgets
│   │   │
│   │   ├── voice/                # Voice control module
│   │   │   ├── __init__.py
│   │   │   └── voice_controller.py  # Voice recognition & TTS
│   │   │
│   │   ├── motion/               # Motion control module
│   │   │   ├── __init__.py
│   │   │   └── gesture_recognizer.py  # Hand gesture recognition
│   │   │
│   │   └── camera/               # Camera control module
│   │       ├── __init__.py
│   │       └── camera_controller.py   # Camera operations
│   │
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── helpers.py            # Helper functions
│
├── web/                          # Web application
│   ├── app.py                    # Flask web app entry point
│   ├── templates/                # HTML templates
│   │   └── index.html
│   └── static/                   # Static files
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
│
├── config/                       # Configuration files
│   ├── __init__.py
│   └── settings.py              # Application settings
│
├── tests/                        # Test files
│   └── __init__.py
│
├── run_desktop.py                # Run desktop application
├── run_web.py                    # Run web application
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
└── PROJECT_STRUCTURE.md          # This file
```

## 🚀 Running the Applications

### Desktop Application
```bash
python run_desktop.py
```

### Web Application
```bash
python run_web.py
```

### CLI API Interface
```bash
python -m src.api.cli
```

## 📦 Module Descriptions

### `src/api/`
Contains all API-related code:
- **gemini_client.py**: Handles Gemini AI integration
- **routes.py**: Flask API endpoints
- **cli.py**: Command-line interface for testing

### `src/desktop/`
Desktop application modules:
- **app.py**: Main application class and GUI setup
- **command_processor.py**: Processes voice and gesture commands
- **gui/**: Reusable GUI components
- **voice/**: Voice recognition and text-to-speech
- **motion/**: Hand gesture recognition using MediaPipe
- **camera/**: Camera capture and processing

### `src/utils/`
Shared utility functions used across modules

### `web/`
Flask web application:
- **app.py**: Flask app initialization and routes
- **templates/**: HTML templates
- **static/**: CSS and JavaScript files

### `config/`
Configuration management:
- **settings.py**: Centralized settings loaded from environment variables

## 🔧 Configuration

All configuration is managed through `config/settings.py` and environment variables:
- `GEMINI_API_KEY`: Your Gemini API key
- `FLASK_HOST`: Flask server host (default: 0.0.0.0)
- `FLASK_PORT`: Flask server port (default: 5000)

## 📝 Code Organization Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Modularity**: Code is split into logical, reusable modules
3. **Configuration Management**: Centralized configuration in `config/`
4. **Entry Points**: Clear entry points for each application mode
5. **Reusability**: Shared utilities and components

## 🔄 Migration from Old Structure

The old files (`app.py`, `main.py`, `.api/new_api.py`) are still present but the new structure uses:
- `web/app.py` instead of `app.py`
- `src/desktop/app.py` instead of `main.py`
- `src/api/new_api.py` instead of `.api/new_api.py`

You can gradually migrate to the new structure or keep both for compatibility.

🧑‍💻 Author
**Tushar Kanti Mahato**
🔹 GitHub: @tusharkantimahato  
🔹 Project: Jarvis 3.0 – Multimodal Assistant
🔹 Version: v3.0
🔹 Python Runtime: py -3.12

💡 Notes


Tested on Windows 10/11


Ensure microphone and camera permissions are granted


Best experience on Python 3.12 with MediaPipe installed



“Jarvis is always ready to assist you — by your voice or motion.”

## 📅 Future Improvements / Update Plan

Jarvis 3.0 is an evolving AI assistant — future updates will focus on performance, stability, and feature enhancement.
If any errors, bugs, or mistakes occur in the current version, they will be corrected and optimized in upcoming releases.

## Planned Enhancements:

🧠 AI Integration: Add NLP & LLM support (ChatGPT / Gemini API) for contextual conversation

🎥 Enhanced Gesture Recognition: Improve motion accuracy and add more gestures

🎙️ Voice Model Upgrade: Faster response and noise reduction

⚙️ Modular Architecture: Split modules for voice, camera, and gesture into separate packages

🌐 Web Connectivity: Enable online information fetching (weather, news, etc.)

🪄 Error Handling: Auto-detect and log exceptions for smoother debugging

💾 Update Tracker: Auto-update system for new versions

🧩 If you modify or upgrade Jarvis 3.0 in the future, please mention the version and date in the changelog section below to keep the project well-documented.

---

⭐ If you like this project, please give it a star — it helps support future updates!
We hope you enjoy using Jarvis 3.0!
