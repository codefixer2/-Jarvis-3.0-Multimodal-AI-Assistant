# 🤖 Jarvis 3.0 – Multimodal AI Assistant

### Description:
Jarvis 3.0 is a smart AI desktop assistant built with Python.
It combines speech recognition, computer vision, and automation to perform tasks like voice control, app launching, gesture recognition, and real-time interaction.

**Jarvis 3.0** is an advanced multimodal desktop assistant built using **Python 3.12**.  
It combines **Voice Recognition**, **Gesture & Motion Control**, and **Camera Interaction** to create a seamless, hands-free assistant experience.

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
git clone https://github.com/<your-username>/Jarvis3.0.git
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

🧾 Project Structure
📁 Jarvis 3.0/
│
├── src/
│   ├── api/
│   │   ├── routes/
│   │   ├── gemini_client.py
│   │   ├── cli.py
│   │   └── __init__.py
│   │
│   ├── desktop/
│   │   ├── main_window.py
│   │   ├── widgets/
│   │   └── __init__.py
│   │
│   ├── gui/
│   │   ├── components/
│   │   ├── layouts/
│   │   └── __init__.py
│   │
│   ├── voice/
│   │   ├── recognizer.py
│   │   ├── text_to_speech.py
│   │   └── __init__.py
│   │
│   ├── motion/
│   │   ├── gesture_recognition.py
│   │   └── __init__.py
│   │
│   ├── camera/
│   │   ├── camera_controller.py
│   │   └── __init__.py
│   │
│   ├── utils/
│   │   ├── helpers.py
│   │   ├── logger.py
│   │   └── __init__.py
│   │
│   ├── web/
│   │   ├── app.py
│   │   ├── templates/
│   │   │   └── *.html
│   │   ├── static/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   │   └── __init__.py
│
├── config/
│   ├── settings.py
│   └── config.yaml
│
├── tests/
│   ├── test_api.py
│   ├── test_desktop.py
│   ├── test_web.py
│   └── __init__.py
│
├── run_desktop.py
├── run_web.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore

🧑‍💻 Author
**Tushar Kanti Mahato**
🔹 GitHub: @codefixer2  
🔹 Project: Jarvis 3.0 – Multimodal Assistant
🔹 Version: v3.0
🔹 Python Runtime: py -3.12

📜 Licensed under the [MIT License](LICENSE)
This project is licensed under the MIT License – you are free to modify and distribute it with attribution.
MIT License © 2025 Tushar Kanti Mahato



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
