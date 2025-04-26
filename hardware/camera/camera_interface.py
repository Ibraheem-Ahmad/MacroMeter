import cv2
import numpy as np
from typing import Optional, Tuple
import time

class CameraInterface:
    def __init__(self, camera_id: int = 0, resolution: Tuple[int, int] = (1920, 1080)):
        """
        Initialize the camera interface.
        
        Args:
            camera_id: ID of the camera device
            resolution: Camera resolution (width, height)
        """
        self.camera_id = camera_id
        self.resolution = resolution
        self.camera = None
        
    def connect(self) -> bool:
        """
        Connect to the camera.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.camera = cv2.VideoCapture(self.camera_id)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            return self.camera.isOpened()
        except Exception as e:
            print(f"Error connecting to camera: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from the camera."""
        if self.camera and self.camera.isOpened():
            self.camera.release()
            
    def capture_image(self) -> Optional[np.ndarray]:
        """
        Capture an image from the camera.
        
        Returns:
            np.ndarray: Captured image, or None if capture failed
        """
        if not self.camera or not self.camera.isOpened():
            return None
            
        try:
            ret, frame = self.camera.read()
            if ret:
                return frame
            return None
        except Exception as e:
            print(f"Error capturing image: {e}")
            return None
            
    def capture_image_with_retry(self, max_retries: int = 3) -> Optional[np.ndarray]:
        """
        Capture an image with retry logic.
        
        Args:
            max_retries: Maximum number of retry attempts
            
        Returns:
            np.ndarray: Captured image, or None if all attempts failed
        """
        for attempt in range(max_retries):
            image = self.capture_image()
            if image is not None:
                return image
            time.sleep(0.1)
        return None
        
    def get_camera_info(self) -> dict:
        """
        Get information about the camera.
        
        Returns:
            dict: Camera information
        """
        if not self.camera or not self.camera.isOpened():
            return {}
            
        info = {
            "width": int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": self.camera.get(cv2.CAP_PROP_FPS),
            "brightness": self.camera.get(cv2.CAP_PROP_BRIGHTNESS),
            "contrast": self.camera.get(cv2.CAP_PROP_CONTRAST),
            "saturation": self.camera.get(cv2.CAP_PROP_SATURATION)
        }
        return info 