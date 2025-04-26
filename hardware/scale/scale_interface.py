import time
from typing import Optional, Callable
import serial
import RPi.GPIO as GPIO

class ScaleInterface:
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 9600):
        """
        Initialize the scale interface.
        
        Args:
            port: Serial port for the scale
            baudrate: Baud rate for serial communication
        """
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.callback = None
        
    def connect(self) -> bool:
        """
        Connect to the scale.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            return True
        except serial.SerialException as e:
            print(f"Error connecting to scale: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from the scale."""
        if self.serial and self.serial.is_open:
            self.serial.close()
            
    def read_weight(self) -> Optional[float]:
        """
        Read the current weight from the scale.
        
        Returns:
            float: Weight in grams, or None if reading failed
        """
        if not self.serial or not self.serial.is_open:
            return None
            
        try:
            # Send command to read weight
            self.serial.write(b'W\r\n')
            response = self.serial.readline().decode().strip()
            
            # Parse response
            try:
                weight = float(response)
                return weight
            except ValueError:
                return None
                
        except serial.SerialException as e:
            print(f"Error reading weight: {e}")
            return None
            
    def set_callback(self, callback: Callable[[float], None]):
        """
        Set a callback function to be called when weight changes.
        
        Args:
            callback: Function to call with new weight value
        """
        self.callback = callback
        
    def start_monitoring(self, interval: float = 0.5):
        """
        Start monitoring weight changes.
        
        Args:
            interval: Time between readings in seconds
        """
        while True:
            weight = self.read_weight()
            if weight is not None and self.callback:
                self.callback(weight)
            time.sleep(interval)
            
    def tare(self) -> bool:
        """
        Tare the scale (set current weight to zero).
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.serial or not self.serial.is_open:
            return False
            
        try:
            self.serial.write(b'T\r\n')
            response = self.serial.readline().decode().strip()
            return response == "OK"
        except serial.SerialException as e:
            print(f"Error taring scale: {e}")
            return False 