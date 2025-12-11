"""Motion/Gesture Recognition Module"""
import numpy as np
import cv2
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False


class GestureRecognizer:
    """Handles hand gesture recognition using MediaPipe"""
    
    def __init__(self):
        if MEDIAPIPE_AVAILABLE:
            self.hands = mp.solutions.hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
            self.mp_hands = mp.solutions.hands
        else:
            self.hands = None
            self.mp_hands = None
    
    def is_available(self):
        """Check if MediaPipe is available"""
        return MEDIAPIPE_AVAILABLE
    
    def recognize_gesture(self, hand_landmarks):
        """Recognize gesture from hand landmarks"""
        if not MEDIAPIPE_AVAILABLE or hand_landmarks is None or self.mp_hands is None:
            return "None"
        
        landmarks = hand_landmarks.landmark
        thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        index_finger_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_finger_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_finger_tip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP]
        
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
    
    def process_frame(self, frame):
        """Process a frame for hand detection"""
        if not MEDIAPIPE_AVAILABLE or self.hands is None:
            return frame, None
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        gesture = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                gesture = self.recognize_gesture(hand_landmarks)
                break  # Process first hand only
        
        return frame, gesture

