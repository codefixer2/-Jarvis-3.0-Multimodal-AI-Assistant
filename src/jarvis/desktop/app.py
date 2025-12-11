"""Desktop Application - Main Entry Point"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import queue
import threading
import time
from PIL import Image, ImageTk
import cv2

from jarvis.desktop.voice.voice_controller import VoiceController
from jarvis.desktop.motion.gesture_recognizer import GestureRecognizer
from jarvis.desktop.camera.camera_controller import CameraController
from jarvis.desktop.command_processor import CommandProcessor
from jarvis.desktop.gui.components import ConsoleWidget
from jarvis.config.settings import (
    DESKTOP_APP_TITLE, DESKTOP_APP_GEOMETRY, DESKTOP_BG_COLOR,
    GESTURE_COOLDOWN
)

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("Warning: mediapipe not available. Motion control features will be disabled.")


class JarvisDesktopApp:
    """Main Desktop Application Class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(DESKTOP_APP_TITLE)
        self.root.geometry(DESKTOP_APP_GEOMETRY)
        self.root.configure(bg=DESKTOP_BG_COLOR)
        
        # Initialize controllers
        self.voice_controller = VoiceController()
        self.gesture_recognizer = GestureRecognizer()
        self.camera_controller = CameraController()
        self.command_processor = CommandProcessor(
            self.camera_controller, 
            self.voice_controller
        )
        
        # State variables
        self.voice_active = False
        self.motion_active = False
        self.last_gesture = None
        self.gesture_cooldown = 0
        
        # MediaPipe drawing utils
        if MEDIAPIPE_AVAILABLE:
            self.drawing_utils = mp.solutions.drawing_utils
            self.mp_hands = mp.solutions.hands
        else:
            self.drawing_utils = None
            self.mp_hands = None
        
        # Setup GUI
        self.setup_gui()
        
        # Message queue for thread-safe GUI updates
        self.message_queue = queue.Queue()
        self.process_messages()
        
        # Calibrate microphone
        success, msg = self.voice_controller.calibrate_microphone()
        if success:
            self.log_message("Microphone calibrated successfully")
        else:
            self.log_message(f"Microphone calibration: {msg}")
    
    def setup_gui(self):
        """Setup the GUI components"""
        # Header frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.X, pady=0, padx=20)
        
        title_label = ttk.Label(
            main_frame, 
            text=DESKTOP_APP_TITLE, 
            font=('Arial', 24, 'bold'), 
            foreground='#00ff00', 
            background=DESKTOP_BG_COLOR
        )
        title_label.pack(side=tk.LEFT, padx=10)
        
        subtitle_label = ttk.Label(
            main_frame, 
            text="(Voice, Motion, Camera Control)", 
            font=('Arial', 14), 
            foreground='#00ff00', 
            background=DESKTOP_BG_COLOR
        )
        subtitle_label.pack(side=tk.LEFT, padx=10)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            main_frame, 
            textvariable=self.status_var, 
            font=('Arial', 12), 
            foreground='#ffff00', 
            background=DESKTOP_BG_COLOR
        )
        status_label.pack(side=tk.RIGHT, padx=10)
        
        # Content frame
        content_frame = ttk.Frame(self.root, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        # Left frame - Camera and controls
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Camera frame
        cam_frame = ttk.LabelFrame(left_frame, text="Camera Feed", padding=10)
        cam_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.camera_label = tk.Label(
            cam_frame, 
            text="Camera Feed\n[Click Start Camera]", 
            bg='#000000', 
            fg='#ffffff', 
            font=('Arial', 12), 
            width=60, 
            height=20
        )
        self.camera_label.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons frame
        control_frame = ttk.Frame(left_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.voice_button = ttk.Button(
            control_frame, 
            text="Start Voice Control", 
            command=self.toggle_voice, 
            width=20
        )
        self.voice_button.pack(side=tk.LEFT, padx=5)
        
        self.motion_button = ttk.Button(
            control_frame, 
            text="Start Motion Control", 
            command=self.toggle_motion, 
            width=20
        )
        self.motion_button.pack(side=tk.LEFT, padx=5)
        
        self.camera_button = ttk.Button(
            control_frame, 
            text="Start Camera", 
            command=self.toggle_camera, 
            width=20
        )
        self.camera_button.pack(side=tk.LEFT, padx=5)
        
        # Status labels
        self.voice_status = tk.Label(
            control_frame, 
            text="Voice: Off", 
            font=('Arial', 12), 
            foreground='green', 
            background=DESKTOP_BG_COLOR
        )
        self.voice_status.pack(side=tk.LEFT, padx=5)
        
        self.motion_status = tk.Label(
            control_frame, 
            text="Motion: Off", 
            font=('Arial', 12), 
            foreground='green', 
            background=DESKTOP_BG_COLOR
        )
        self.motion_status.pack(side=tk.LEFT, padx=5)
        
        self.camera_status = tk.Label(
            control_frame, 
            text="Camera: Off", 
            font=('Arial', 12), 
            foreground='green', 
            background=DESKTOP_BG_COLOR
        )
        self.camera_status.pack(side=tk.LEFT, padx=5)
        
        # Right frame - Console
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        console_frame = ttk.LabelFrame(right_frame, text="Jarvis Console", padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        self.console_widget = ConsoleWidget(console_frame)
        self.console_widget.log("JARVIS 3.0 - Initialized...")
        self.console_widget.log("System ready for voice and motion commands")
        
        # Gesture info frame
        gesture_frame = ttk.LabelFrame(right_frame, text="Gesture Information", padding=10)
        gesture_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.current_gesture = tk.StringVar(value="Current Gesture: None")
        gesture_label = tk.Label(
            gesture_frame, 
            textvariable=self.current_gesture, 
            font=('Arial', 12), 
            foreground="#00aaff", 
            background=DESKTOP_BG_COLOR
        )
        gesture_label.pack(side=tk.TOP, padx=0, pady=5)
    
    def toggle_voice(self):
        """Toggle voice control"""
        if not self.voice_active:
            self.voice_active = True
            self.voice_button.config(text="Stop Voice Control")
            self.voice_status.config(text="Voice: On", fg='green')
            self.start_voice_control()
            # Auto-start camera for voice control
            if not self.camera_controller.is_active():
                self.toggle_camera()
        else:
            self.voice_active = False
            self.voice_button.config(text="Start Voice Control")
            self.voice_status.config(text="Voice: Off", fg='red')
            self.log_message("Voice control stopped")
    
    def toggle_camera(self):
        """Toggle camera control"""
        if not self.camera_controller.is_active():
            success, msg = self.camera_controller.start_camera()
            if success:
                self.camera_button.config(text="Stop Camera")
                self.camera_status.config(text="Camera: On", fg='green')
                self.log_message("Camera started")
                self.update_camera_feed()
            else:
                self.log_message(f"Camera failed: {msg}")
        else:
            self.camera_controller.stop_camera()
            self.camera_button.config(text="Start Camera")
            self.camera_status.config(text="Camera: Off", fg='red')
            self.camera_label.config(image='', text="Camera Feed\n[Click Start Camera]")
            self.log_message("Camera stopped")
    
    def toggle_motion(self):
        """Toggle motion control"""
        if not MEDIAPIPE_AVAILABLE:
            self.log_message("Motion control requires MediaPipe. Please install it.")
            return
        
        if not self.motion_active:
            if not self.camera_controller.is_active():
                self.toggle_camera()
            if self.camera_controller.is_active():
                self.motion_active = True
                self.motion_button.config(text="Stop Motion Control")
                self.motion_status.config(text="Motion: On", fg='green')
                self.log_message("Motion control started")
            else:
                self.log_message("Cannot start motion control: Camera not available")
        else:
            self.motion_active = False
            self.motion_button.config(text="Start Motion Control")
            self.motion_status.config(text="Motion: Off", fg='red')
            self.log_message("Motion control stopped")
    
    def start_voice_control(self):
        """Start voice control in a separate thread"""
        if not self.voice_controller.microphone_available:
            self.log_message("Voice control cannot start: Microphone not available")
            return
        
        def voice_loop():
            while self.voice_active:
                command, error = self.voice_controller.listen_for_command()
                if command:
                    self.log_message(f"Voice command: {command}")
                    success, msg = self.command_processor.process_voice_command(command)
                    self.log_message(msg)
                    if self.voice_controller:
                        self.voice_controller.speak_text(msg)
                elif error and "No speech detected" not in error:
                    self.log_message(f"Voice error: {error}")
                time.sleep(0.1)
        
        threading.Thread(target=voice_loop, daemon=True).start()
    
    def update_camera_feed(self):
        """Update camera feed display"""
        if self.camera_controller.is_active():
            frame, error = self.camera_controller.read_frame()
            if frame is not None:
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
                if error:
                    self.log_message(f"Camera error: {error}")
            
            self.root.after(10, self.update_camera_feed)
    
    def process_hand_gestures(self, frame):
        """Process hand gestures in frame"""
        if not MEDIAPIPE_AVAILABLE or not self.gesture_recognizer.is_available():
            return frame
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.gesture_recognizer.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                if self.drawing_utils:
                    self.drawing_utils.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )
                
                # Process gestures
                if self.gesture_cooldown <= 0:
                    gesture = self.gesture_recognizer.recognize_gesture(hand_landmarks)
                    if gesture != self.last_gesture and gesture != "None":
                        self.handle_gesture(gesture)
                        self.last_gesture = gesture
                        self.gesture_cooldown = GESTURE_COOLDOWN
                
                self.gesture_cooldown = max(0, self.gesture_cooldown - 1)
                break  # Process first hand only
        
        return frame
    
    def handle_gesture(self, gesture):
        """Handle gesture commands"""
        self.current_gesture.set(f"Current Gesture: {gesture}")
        success, msg = self.command_processor.process_gesture(gesture)
        self.log_message(f"Gesture: {gesture} - {msg}")
    
    def process_messages(self):
        """Process messages from queue for thread-safe GUI updates"""
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.console_widget.log(message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_messages)
    
    def log_message(self, message):
        """Log a message thread-safely"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_entry = f"[{timestamp}] {message}"
        self.message_queue.put(log_entry)
    
    def on_closing(self):
        """Handle application closing"""
        self.voice_active = False
        self.motion_active = False
        self.camera_controller.release()
        cv2.destroyAllWindows()
        self.root.destroy()


def main():
    """Main entry point for desktop application"""
    root = tk.Tk()
    app = JarvisDesktopApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()


