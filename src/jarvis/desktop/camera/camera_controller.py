"""Camera Control Module"""
import cv2
import time


class CameraController:
    """Handles camera operations"""
    
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.camera_active = False
    
    def start_camera(self):
        """Start camera capture"""
        if self.cap is None:
            try:
                self.cap = cv2.VideoCapture(self.camera_index)
                if self.cap.isOpened():
                    self.camera_active = True
                    return True, "Camera started successfully"
                else:
                    return False, "Failed to open camera"
            except Exception as e:
                return False, f"Failed to start camera: {str(e)}"
        return True, "Camera already started"
    
    def stop_camera(self):
        """Stop camera capture"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.camera_active = False
    
    def read_frame(self):
        """Read a frame from the camera"""
        if self.cap is None or not self.camera_active:
            return None, None
        
        ret, frame = self.cap.read()
        if ret:
            return frame, None
        else:
            return None, "Failed to read frame"
    
    def is_active(self):
        """Check if camera is active"""
        return self.camera_active
    
    def release(self):
        """Release camera resources"""
        self.stop_camera()


