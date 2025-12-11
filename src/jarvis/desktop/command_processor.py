"""Command Processing Module for Desktop App"""
import pyautogui
import keyboard
import time
import cv2
from jarvis.utils.helpers import open_application


class CommandProcessor:
    """Processes voice and gesture commands"""
    
    def __init__(self, camera_controller=None, voice_controller=None):
        self.camera_controller = camera_controller
        self.voice_controller = voice_controller
    
    def process_voice_command(self, command):
        """Process a voice command"""
        command_lower = command.lower()
        
        if "start camera" in command_lower or "open camera" in command_lower:
            if self.camera_controller:
                success, msg = self.camera_controller.start_camera()
                return success, msg
        elif "stop camera" in command_lower:
            if self.camera_controller:
                self.camera_controller.stop_camera()
                return True, "Camera stopped"
        elif "volume up" in command_lower:
            self.volume_up()
            return True, "Volume increased"
        elif "volume down" in command_lower:
            self.volume_down()
            return True, "Volume decreased"
        elif "mute volume" in command_lower:
            self.mute_volume()
            return True, "Volume muted"
        elif "unmute volume" in command_lower:
            self.unmute_volume()
            return True, "Volume unmuted"
        elif "take picture" in command_lower or "take screenshot" in command_lower:
            self.take_screenshot()
            return True, "Screenshot taken"
        elif "scroll up" in command_lower:
            self.scroll_up()
            return True, "Scrolled up"
        elif "scroll down" in command_lower:
            self.scroll_down()
            return True, "Scrolled down"
        elif "what is the time" in command_lower or "tell time" in command_lower:
            return True, self.tell_time()
        elif "open" in command_lower:
            words = command_lower.split()
            if "open" in words:
                idx = words.index("open")
                if idx + 1 < len(words):
                    app_name = words[idx + 1]
                    success, msg = open_application(app_name)
                    return success, msg
        
        return False, f"Unknown command: {command}"
    
    def process_gesture(self, gesture):
        """Process a gesture command"""
        if gesture == "thumbs down":
            self.volume_down()
            return True, "Volume decreased"
        elif gesture == "open palm":
            keyboard.press_and_release('play/pause media')
            return True, "Media play/pause toggled"
        elif gesture == "pointing up":
            # Handle pointing gesture
            return True, "Pointing detected"
        else:
            return False, f"Unknown gesture: {gesture}"
    
    def volume_up(self):
        """Increase volume"""
        for _ in range(5):
            pyautogui.press("volumeup")
    
    def volume_down(self):
        """Decrease volume"""
        for _ in range(5):
            pyautogui.press("volumedown")
    
    def mute_volume(self):
        """Mute volume"""
        for _ in range(5):
            pyautogui.press("volumemute")
    
    def unmute_volume(self):
        """Unmute volume"""
        for _ in range(5):
            pyautogui.press("volumemute")
    
    def take_screenshot(self):
        """Take a screenshot"""
        filename = f"screenshot_{int(time.time())}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return filename
    
    def take_picture(self):
        """Take a picture from camera"""
        if self.camera_controller and self.camera_controller.is_active():
            frame, error = self.camera_controller.read_frame()
            if frame is not None:
                filename = f"picture_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                return True, f"Picture saved as {filename}"
            else:
                return False, error or "Failed to capture frame"
        return False, "Camera not active"
    
    def scroll_up(self):
        """Scroll up"""
        pyautogui.scroll(3)
    
    def scroll_down(self):
        """Scroll down"""
        pyautogui.scroll(-3)
    
    def tell_time(self):
        """Get current time"""
        current_time = time.strftime("%I:%M %p")
        return f"The current time is {current_time}"


