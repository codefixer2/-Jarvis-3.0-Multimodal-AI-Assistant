import tkinter as tk
from tkinter import ttk, scrolledtext
import queue
import cv2
try:
    import mediapipe as mp   # pyright: ignore[reportMissingImports]
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("Warning: mediapipe not available. Motion control features will be disabled.")
    print("Please install mediapipe using: pip install mediapipe")
    print("Note: mediapipe may not be available for Python 3.13. Consider using Python 3.11 or earlier.")
import pyautogui
import speech_recognition as sr
import threading
import time
import json
import os
import pyttsx3
from PIL import Image, ImageTk  
import numpy as np
import screeninfo
import keyboard

class JarvisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis 3.0 - multimodel Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a1a')
        
        self.voice_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
            self.microphone_available = True
        except (AttributeError, OSError) as e:
            print(f"Warning: Microphone not available: {e}")
            print("Voice control features will be limited.")
            self.microphone = None
            self.microphone_available = False
        
        if MEDIAPIPE_AVAILABLE:
            self.hands = mp.solutions.hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
            self.np_pose = mp.solutions.pose
            self.drawing_utils = mp.solutions.drawing_utils
        else:
            self.hands = None
            self.np_pose = None
            self.drawing_utils = None
        
        self.voice_active = False
        self.motion_active = False
        self.camera_active = False
        self.cap = None
        
        self.last_gesture = None
        self.gesture_cooldown = 0
        
        self.setup_gui()
        
        self.message_queue = queue.Queue()
        self.process_queue = queue.Queue()
        self.process_messages()
        
        self.calibrate_microphone()
        
    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.X, pady=0, padx=20)

        title_label=ttk.Label(main_frame, text="Jarvis 3.0 - multimodel Assistant", font=('Arial', 24, 'bold'), foreground='#00ff00', background='#0a0a1a')
        title_label.pack(side=tk.LEFT, padx=10)
        
        subtitle_label=ttk.Label(main_frame, text="(Voice, Motion, Camera Control)", font=('Arial', 14), foreground='#00ff00', background='#0a0a1a')
        subtitle_label.pack(side=tk.LEFT, padx=10)

        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=('Arial', 12), foreground='#ffff00', background='#0a0a1a')
        status_label.pack(side=tk.RIGHT, padx=10)

        content_frame = ttk.Frame(self.root, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        cam_frame= ttk.LabelFrame(left_frame , text = "Motion Capture Feed" , padding=10)
        cam_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))
        self.camera_label = tk.Label(cam_frame, text="Camera Feed\n[Click Start Camera]", bg='#000000', fg='#ffffff', font=('Arial', 12), width=60, height=20)
        self.camera_label.pack(fill=tk.BOTH, expand=True)
        
        control_frame = ttk.Frame(left_frame)
        control_frame.pack(fill=tk.X, pady=(0,10))
        self.voice_button = ttk.Button(control_frame, text="StartVoice Control", command=self.toggle_voice, width=20)
        self.voice_button.pack(side=tk.LEFT, padx=5)
        self.motion_button = ttk.Button(control_frame, text="Start Motion Control", command=self.toggle_motion, width=20)
        self.motion_button.pack(side=tk.LEFT, padx=5)
        self.camera_button = ttk.Button(control_frame, text="Start Camera Control", command=self.toggle_camera, width=20)
        self.camera_button.pack(side=tk.LEFT, padx=5)
        self.voice_status = tk.Label(control_frame, text="Voice: Off", font=('Arial', 12), foreground='green', background='#0a0a1a')
        self.voice_status.pack(side=tk.LEFT, padx=5)
        self.motion_status = tk.Label(control_frame, text="Motion: Off", font=('Arial', 12), foreground='green', background='#0a0a1a')
        self.motion_status.pack(side=tk.LEFT, padx=5)
        self.camera_status = tk.Label(control_frame, text="Camera: Off", font=('Arial', 12), foreground='green', background='#0a0a1a')
        self.camera_status.pack(side=tk.LEFT, padx=5)
        motion_frame= ttk.LabelFrame(left_frame , text = "Motion Capture Feed" , padding=10)
        motion_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))
        self.motion_button = ttk.Button(motion_frame, text="Start Motion Control", command=self.toggle_motion, width=20)
        self.motion_button.pack(side=tk.LEFT, padx=0, pady=5)
        self.motion_status = tk.Label(motion_frame, text="Motion: Off", font=('Arial', 12), foreground='green', background='#0a0a1a')
        self.motion_status.pack(side=tk.LEFT, padx=0, pady=5)
        self.camera_button = ttk.Button(motion_frame, text="Start Camera Control", command=self.toggle_camera, width=20)
        self.camera_button.pack(side=tk.RIGHT, padx=0, pady=5)
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        right_frame_inner = ttk.Frame(right_frame, padding="10")
        right_frame_inner.pack(fill=tk.BOTH, expand=True)
        Console_frame = ttk.LabelFrame(right_frame_inner, text=" JarvisConsole", padding=10)
        Console_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))
        Console_label = tk.Label(Console_frame, text=" JarvisConsole", font=('Arial', 12), foreground='#00ff00', background='#0a0a1a')
        Console_label.pack(side=tk.TOP, padx=0, pady=5)
        self.console = scrolledtext.ScrolledText(Console_frame, width=60, height=15, font=('Arial', 12), state=tk.DISABLED, bg='#000000', fg='#ffffff', insertbackground='#ffffff')    
        self.console.pack(fill=tk.BOTH, expand=True)
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END,"JARVIS 3.0 - Initialized...\n") 
        self.console.insert(tk.END,"System ready for voice and motion commands\n")
        self.console.insert(tk.END,"Welcome to Jarvis Console\n")
        self.console.insert(tk.END,"Jarvis is ready to assist you\n")
        self.console.insert(tk.END,"Jarvis ready to help you simply by your voice or motion:\n")
        self.console.insert(tk.END,"You can start by saying 'Hello Jarvis' or 'Start Voice Control'\n")
        self.console.insert(tk.END,"or by moving your hand in front of the camera\n")
        self.console.insert(tk.END,"or by using the motion control buttons\n")
        self.console.insert(tk.END,"or by using the camera control buttons\n")
        self.console.insert(tk.END,"or by using the console control buttons\n")
        self.console.insert(tk.END,"Jarvis is waiting for your command...\n")
        self.console.insert(tk.END,"What can I do for you today?\n")
        self.console.insert(tk.END,"What is the weather in purulia?\n")
        self.console.insert(tk.END,"What is the weather in kolkata?\n")
        self.console.insert(tk.END,"What is the weather in mumbai?\n")
        self.console.insert(tk.END,"What is the weather in delhi?\n")
        self.console.insert(tk.END,"What is the weather in bangalore?\n")
        self.console.insert(tk.END,"What is the weather in chennai?\n")
        self.console.insert(tk.END,"What is the weather in hyderabad?\n")
        self.console.insert(tk.END,"What is the weather in pune?\n")
        self.console.insert(tk.END,"who made you?\n")
        self.console.insert(tk.END,"I am made by codefixer2\n")
        self.console.insert(tk.END,"Jarvis is made by codefixer2?\n")
        self.console.insert(tk.END,"Jarvis tell me a joke?\n")
        self.console.insert(tk.END,"for more information, please visit the Jarvis website at https://www.jarvis.com\n")
        self.console.config(state=tk.DISABLED)
        
        info_frame = ttk.Frame(right_frame_inner)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_text = tk.Text(info_frame, height=10, width=50, font=('Arial', 12), bg='#000000', fg='#ffffff', insertbackground='#ffffff', wrap=tk.WORD)
        info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_text.config(state=tk.DISABLED)

        gesture_frame = ttk.LabelFrame(right_frame_inner, text="Gesture Information", padding=10)
        gesture_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))
        
        self.current_gesture = tk.StringVar(value="Current Gesture: None")
        gesture_label = tk.Label(gesture_frame, textvariable=self.current_gesture, font=('Arial', 12), foreground="#00aaff", background='#0a0a1a')
        gesture_label.pack(side=tk.TOP, padx=0, pady=5)
        
    def update_camera_feed(self):
        if self.camera_active and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                # Process hand gestures if motion control is active
                if self.motion_active and MEDIAPIPE_AVAILABLE:
                    frame = self.process_hand_gestures(frame)
                
                # Convert frame for display
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                
                self.camera_label.config(image=img)
                self.camera_label.image = img
            else:
                # Camera read failed, try to reinitialize
                if self.camera_active:
                    self.log_message("Camera read failed, attempting to reinitialize...")
                    try:
                        self.cap.release()
                        self.cap = cv2.VideoCapture(0)
                    except Exception as e:
                        self.log_message(f"Camera reinitialization failed: {str(e)}")
            
            self.root.after(10, self.update_camera_feed)

    def process_hand_gestures(self, frame):
        if not MEDIAPIPE_AVAILABLE or self.hands is None:
            return frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                if self.drawing_utils:
                    self.drawing_utils.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp.solutions.hands.HAND_CONNECTIONS
                    )
                
                # Process gestures
                if self.gesture_cooldown <= 0:
                    gesture = self.recognize_gesture(hand_landmarks)
                    if gesture != self.last_gesture:
                        self.handle_gesture(gesture)
                        self.last_gesture = gesture
                        self.gesture_cooldown = 20  # Prevent rapid gesture changes
                
                self.gesture_cooldown = max(0, self.gesture_cooldown - 1)
        
        return frame

    def calibrate_microphone(self):
        if not self.microphone_available or self.microphone is None:
            self.log_message("Microphone calibration skipped: Microphone not available")
            return
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            self.update_console("Microphone calibrated for ambient noise.")
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio)
                self.log_message("Microphone Calibrated. Initial command: " + command)
                self.update_console(f"Initial command recognized: {command}")
                
        except Exception as e:
            self.log_message("Microphone calibration failed: " + str(e))
    
    def toggle_voice(self):
        """toggle voice control on or off"""
        if not self.voice_active:
            self.voice_active = True
            self.voice_button.config(text="Stop Voice Control")
            self.voice_status.config(text="Voice: On", fg='green')
            self.start_voice_control()
            self.camera_active = True
            self.start_camera()
        else:
            self.voice_active = False
            self.voice_button.config(text="Start Voice Control")
            self.voice_status.config(text="Voice: Off", fg='red')
            self.log_message("Voice control stopped by user.")
            threading.Thread(target=self.stop_voice_control, daemon=True).start()
    
    def toggle_camera(self):
        """toggle camera control on or off"""
        if not self.camera_active:
            try:
                self.cap = cv2.VideoCapture(0)
                self.camera_active = True
                self.camera_button.config(text="Stop Camera Control")
                self.camera_status.config(text="Camera: On", fg='green')
                self.update_camera_feed()
                self.log_message("Camera control started.")
                threading.Thread(target=self.update_camera_feed, daemon=True).start()
            except Exception as e:
                self.log_message("Camera initialization failed: " + str(e))
        else:
            self.stop_camera()
    
    def stop_camera(self):
        """Stop camera control"""
        if self.camera_active:
            self.camera_active = False
            if self.cap is not None:
                self.cap.release()
                self.cap = None
            self.camera_button.config(text="Start Camera Control", fg='red')
            self.camera_label.config(image='', text="Camera Feed\n[Click Start Camera]")
            self.camera_status.config(text="Camera: Off", fg='red')
            self.log_message("Camera control stopped by user.")
            threading.Thread(target=self.release_camera, daemon=True).start()
    
    def voice_listening_loop(self):
        """Continuously listen for voice commands"""
        if not self.microphone_available or self.microphone is None:
            self.log_message("Voice listening loop stopped: Microphone not available")
            return
        while self.voice_active:
            try:
                with self.microphone as source:
                    self.update_console("Listening for command...")
                    audio = self.recognizer.listen(source, timeout=5)
                    command = self.recognizer.recognize_google(audio)
                    command = command.lower()
                    self.log_message("Voice command recognized: " + command)
                    self.update_console(f"Command: {command}")
                    self.process_voice_command(command)
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                self.log_message("Could not understand the audio")
            except sr.RequestError as e:
                self.log_message("Could not request results; {0}".format(e))
            except Exception as e:
                self.log_message("Voice listening error: " + str(e))
            time.sleep(0.1)
    
    def process_voice_command(self, command):
        """Process recognized voice command"""
        try:
            self.log_message("Processing voice command: " + command)
            if "start camera" in command or "open camera" in command:
                self.start_camera()
            elif "stop camera" in command:
                self.stop_camera()
            elif "volume up" in command:
                self.volume_up()
            elif "volume down" in command:
                self.volume_down()
            elif "mute volume" in command:
                self.mute_volume()
            elif "unmute volume" in command:
                self.unmute_volume()
            elif "take picture" in command or "take screenshot" in command:
                self.take_picture()
            elif "record video" in command:
                self.record_video()
            elif "stop video" in command:
                self.stop_video()
            elif "scroll up" in command:
                self.scroll_up()
            elif "scroll down" in command:
                self.scroll_down()
            elif "what is the time" in command or "tell time" in command:
                self.tell_time()
            elif "open" in command:
                # Extract app name from command
                words = command.split()
                if "open" in words:
                    idx = words.index("open")
                    if idx + 1 < len(words):
                        app_name = words[idx + 1]
                        self.open_application(app_name)
            else:
                self.log_message("Unknown command: " + command)
        except Exception as e:
            self.log_message("Error processing command: " + str(e))
    
    def open_application(self, app_name):
        """Open an application by name"""
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "camera": "microsoft.windows.camera:",
            "browser": 'chrome.exe',
            "OpenAI": "C:\\Program Files\\OpenAI\\OpenAI.exe",
            "Brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            "Discord": "C:\\Program Files\\Discord\\Discord.exe",
            "WhatsApp": "C:\\Program Files\\WhatsApp\\WhatsApp.exe",
            "Telegram": "C:\\Program Files\\Telegram\\Telegram.exe",
            "Skype": "C:\\Program Files\\Skype\\Skype.exe",
            "Zoom": "C:\\Program Files\\Zoom\\Zoom.exe",
            "Microsoft Teams": "C:\\Program Files\\Microsoft Teams\\Teams.exe",
            "Microsoft Edge": "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
            "Microsoft Word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
            "Microsoft Excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
            "Microsoft PowerPoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
            "Microsoft OneNote": "C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE",
            "Microsoft Outlook": "C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE",
            "whatsapp": "C:\\Program Files\\WhatsApp\\WhatsApp.exe",
            "youtube": "C:\\Program Files\\Youtube\\Youtube.exe",
            "facebook": "C:\\Program Files\\Facebook\\Facebook.exe",
            "Chrome": "C:\\Program Files\\Chrome\\Chrome.exe",
            "twitter": "C:\\Program Files\\Twitter\\Twitter.exe",
            "linkedin": "C:\\Program Files\\LinkedIn\\LinkedIn.exe",
            "github": "C:\\Program Files\\GitHub\\GitHub.exe",
            "gitlab": "C:\\Program Files\\GitLab\\GitLab.exe",
        }
        app_path = apps.get(app_name.lower())
        if app_path:
            try:
                os.startfile(app_path)
                self.log_message(f"Opened application: {app_name}")
                self.speak_text(f"Opening {app_name}")
            except Exception as e:
                self.log_message(f"Failed to open application {app_name}: {str(e)}")
        else:
            self.log_message(f"Application not found in my database: {app_name}")

    def volume_up(self):
        """Increase the volume"""
        self.log_message("Volume up")
        self.speak_text("Increasing volume")
        for _ in range(5):
            pyautogui.press("volumeup")

    def volume_down(self):
        """Decrease the volume"""
        self.log_message("Volume down")
        self.speak_text("Decreasing volume")
        for _ in range(5):
            pyautogui.press("volumedown")

    def mute_volume(self):
        """Mute the volume"""
        self.log_message("Mute volume")
        self.speak_text("Muting volume")
        for _ in range(5):
            pyautogui.press("volumemute")

    def unmute_volume(self):
        """Unmute the volume"""
        self.log_message("Unmute volume")
        self.speak_text("Unmuting volume")
        for _ in range(5):
            pyautogui.press("volumemute")
    
    def take_screenshot(self):
        """Take a screenshot"""
        self.log_message("Taking screenshot")
        self.speak_text("Taking screenshot")
        filename = f"screenshot_{int(time.time())}.png"
        self.speak_text(f"Saving screenshot as {filename}")
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)

    def take_picture(self):
        """Take a picture from camera"""
        if self.camera_active and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                filename = f"picture_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                self.log_message(f"Picture saved as {filename}")
                self.speak_text(f"Picture saved as {filename}")

    def record_video(self):
        """Start recording video"""
        self.log_message("Recording video started")
        self.speak_text("Recording video")
        # Video recording implementation would go here

    def stop_video(self):
        """Stop recording video"""
        self.log_message("Recording video stopped")
        self.speak_text("Recording stopped")

    def scroll_up(self):
        """Scroll up"""
        self.log_message("Scrolling up")
        pyautogui.scroll(3)

    def scroll_down(self):
        """Scroll down"""
        self.log_message("Scrolling down")
        pyautogui.scroll(-3)

    def tell_time(self):
        """Tell the current time"""
        current_time = time.strftime("%I:%M %p")
        self.log_message(f"Current time: {current_time}")
        self.speak_text(f"The current time is {current_time}")

    def explain_capabilities(self):
        """Explain the capabilities of the assistant"""
        self.log_message("Explaining capabilities")
        self.speak_text("I can assist you with various tasks such as opening applications, taking screenshots, and controlling system volume.")
        self.speak_text("I can also help you with tasks like playing music, setting reminders, and providing information.")
        self.speak_text("Feel free to ask me anything or give me commands to perform tasks for you.")
        self.speak_text("I am made by codefixer2.")
        self.speak_text("I am trained by codefixer2 to assist you with your daily tasks.")
        self.speak_text("I am constantly learning and improving to better serve you.")
        self.speak_text("I am also RoastAI certified. Haha!")
        self.speak_text("For more information, please visit the Jarvis website at https://www.jarvis.com.")
    
    def start_voice_control(self):
        """Start voice control"""
        if not self.microphone_available or self.microphone is None:
            self.log_message("Cannot start voice control: Microphone not available")
            self.speak_text("Voice control cannot start. Microphone is not available.")
            return
        self.log_message("Voice control started")
        self.voice_active = True
        threading.Thread(target=self.voice_listening_loop, daemon=True).start()

    def stop_voice_control(self):
        """Stop voice control"""
        self.log_message("Voice control stopped")
        self.voice_active = False

    def start_camera(self):
        """Start camera"""
        if self.cap is None:
            try:
                self.cap = cv2.VideoCapture(0)
                self.camera_active = True
                self.log_message("Camera started")
                self.update_camera_feed()
            except Exception as e:
                self.log_message(f"Failed to start camera: {str(e)}")

    def toggle_motion(self):
        """Toggle motion control"""
        if not MEDIAPIPE_AVAILABLE:
            error_msg = "Motion control requires MediaPipe. Please install it using Python 3.11 or 3.12."
            self.log_message(error_msg)
            self.speak_text("Motion control is not available. MediaPipe is not installed. Please use Python 3.11 or 3.12 to install MediaPipe.")
            self.update_console("ERROR: MediaPipe not available. Motion control disabled.")
            self.update_console("Solution: Install Python 3.11 or 3.12, then run: pip install mediapipe")
            return
        if not self.motion_active:
            # Ensure camera is active for motion detection
            if not self.camera_active:
                self.start_camera()
            if not self.camera_active or self.cap is None:
                self.log_message("Cannot start motion control: Camera not available")
                self.speak_text("Cannot start motion control. Please start camera first.")
                return
            self.motion_active = True
            self.motion_button.config(text="Stop Motion Control")
            self.motion_status.config(text="Motion: On", fg='green')
            self.log_message("Motion control started")
            self.speak_text("Motion control activated")
        else:
            self.motion_active = False
            self.motion_button.config(text="Start Motion Control")
            self.motion_status.config(text="Motion: Off", fg='red')
            self.log_message("Motion control stopped")
            self.speak_text("Motion control deactivated")

    def release_camera(self):
        """Release camera resources"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def speak_text(self, text):
        """Speak the given text using the text-to-speech engine"""
        self.log_message(f"Speaking text: {text}")
        try:
            self.voice_engine.say(text)
            self.voice_engine.runAndWait()
        except Exception as e:
            self.log_message(f"Error speaking text: {str(e)}")

    def update_camera_feed_mp(self):
        """Update the camera feed Mediapipe processing"""
        if not MEDIAPIPE_AVAILABLE:
            return
        mp_hands = mp.solutions.hands
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        ) as hands:
            while self.camera_active:
                ret, frame = self.cap.read()
                if not ret:
                    self.log_message("Failed to grab frame from camera.")
                    break
                mp_pose = mp.solutions.pose
                with mp_pose.Pose(
                    static_image_mode=False,
                    model_complexity=2,
                    enable_segmentation=True,
                    min_detection_confidence=0.7,
                    min_tracking_confidence=0.5
                ) as pose:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = pose.process(rgb_frame)
                # Process hands
                hands_results = hands.process(rgb_frame)
                if hands_results.multi_hand_landmarks and self.drawing_utils:
                    for hand_landmarks in hands_results.multi_hand_landmarks:
                        self.drawing_utils.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp.solutions.hands.HAND_CONNECTIONS
                        )
                # Flip the frame horizontally for a later selfie-view display
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process the frame and detect hands
                results = hands.process(rgb_frame)
                
                # Draw hand landmarks
                if results.multi_hand_landmarks and self.drawing_utils:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.drawing_utils.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp.solutions.hands.HAND_CONNECTIONS
                        )
                if self.motion_active:
                    frame = self.process_hand_gestures(frame)
                    if self.gesture_cooldown <= 0:
                        gesture = self.recognize_gesture(hand_landmarks)
                        if gesture != self.last_gesture:
                            self.handle_gesture(gesture)
                            self.last_gesture = gesture
                            self.gesture_cooldown = 20  # Prevent rapid gesture changes
                self.gesture_cooldown = max(0, self.gesture_cooldown - 1)   
                if results.pose_landmarks and self.drawing_utils and self.np_pose:
                    self.drawing_utils.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        self.np_pose.POSE_CONNECTIONS
                    )
                # Convert frame to ImageTk format
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = ImageTk.PhotoImage(image=img)
                
                # Update the camera label
                self.camera_label.config(image=img)
                self.camera_label.image = img
                self.message_queue.put("Camera feed updated.")
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break  
                time.sleep(0.03)  # Small delay to control frame rate
    
    def process_gesture(self, hand_landmarks, frame):
        """Process hand gestures from landmarks"""
        if hand_landmarpks is None:  # pyright: ignore[reportUndefinedVariable]
            return frame
        if self.motion_active:
            frame = self.process_hand_gestures(frame)
            if self.gesture_cooldown <= 0:
                gesture = self.recognize_gesture(hand_landmarks)
                if gesture != self.last_gesture and gesture != "None":
                    self.handle_gesture(gesture)
                    self.last_gesture = gesture
                    self.gesture_cooldown = 20  # Prevent rapid gesture changes
        self.gesture_cooldown = max(0, self.gesture_cooldown - 1)
        return frame

    def handle_gesture(self, gesture):
        """Handle different hand gestures"""
        if gesture == "pointing up":
            # This will be handled in process_hand_gestures
            pass
        elif gesture == "thumbs down":
            self.volume_down()
            self.gesture_cooldown = 20
        elif gesture == "open palm":
            keyboard.press_and_release('play/pause media')
            self.gesture_cooldown = 10

    def recognize_gesture(self, hand_landmarks):
        """Recognize gesture from hand landmarks"""
        if not MEDIAPIPE_AVAILABLE or hand_landmarks is None:
            return "None"
        landmarks = hand_landmarks.landmark
        thumb_tip = landmarks[mp.solutions.hands.HandLandmark.THUMB_TIP]
        index_finger_tip = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
        middle_finger_tip = landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_finger_tip = landmarks[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = landmarks[mp.solutions.hands.HandLandmark.PINKY_TIP]
        
        thumb_index_dist = np.sqrt(
            (thumb_tip.x - index_finger_tip.x)**2 + 
            (thumb_tip.y - index_finger_tip.y)**2
        )
        
        thumb_tip_y = thumb_tip.y
        index_tip_y = index_finger_tip.y
        middle_tip_y = middle_finger_tip.y
        ring_tip_y = ring_finger_tip.y
        pinky_tip_y = pinky_tip.y
        
        # Check for thumbs down
        if (thumb_tip_y > index_tip_y and 
            thumb_tip_y > middle_tip_y and
            thumb_tip_y > ring_tip_y and 
            thumb_tip_y > pinky_tip_y):
            return "thumbs down"
        
        # Check for pointing
        if thumb_index_dist < 0.05:
            return "pointing up"
        
        # Check for open palm
        all_extended = (index_tip_y < middle_tip_y < ring_tip_y < pinky_tip_y and 
                       thumb_tip.x < index_finger_tip.x)
        if all_extended:
            return "open palm"
        
        return "Unknown"
    
    def process_messages(self):
        """Process messages from the queue and update GUI"""
        try:
            while True:
                message = self.message_queue.get_nowait()
                if isinstance(message, tuple) and len(message) == 2:
                    msg_type, msg_content = message
                    if msg_type == 'camera':
                        self.camera_label.config(text=msg_content)
                    elif msg_type == 'console':
                        self.console.config(state=tk.NORMAL)
                        self.console.insert(tk.END, msg_content + "\n")
                        self.console.see(tk.END)
                        self.console.config(state=tk.DISABLED)
                else:
                    self.console.config(state=tk.NORMAL)
                    self.console.insert(tk.END, str(message) + "\n")
                    self.console.see(tk.END)
                    self.console.config(state=tk.DISABLED)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_messages)
    
    def log_message(self, message):
        """Log a message to the console"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_entry = f"[{timestamp}] {message}"
        self.message_queue.put(('console', log_entry))
    
    def update_console(self, message):
        """Update the console text area"""
        self.message_queue.put(('console', message))
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
    
    def on_closing(self):
        """Handle application closing/clean up when closing application"""
        self.voice_active = False
        self.motion_active = False
        self.camera_active = False
        if self.cap is not None:
            self.cap.release()
            cv2.destroyAllWindows()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = JarvisApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
        