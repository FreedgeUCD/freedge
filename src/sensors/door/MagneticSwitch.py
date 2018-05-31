import RPi.GPIO as GPIO
from ..Sensor import Sensor

class MagneticSwitch(Sensor):
    def __init__(self,  pin, **kwargs):
        self.pin = pin
        super(MagneticSwitch, self).__init__(**kwargs)
        
        # Rasp Pi 3B GPIO Pinout:
        # Ref: http://pi4j.com/pins/model-3b-rev1.html
        GPIO.setmode(GPIO.BCM)

        # Set up the door sensor pin.
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

    def is_open(self):
        # 0 : Close // 1 : Open
        return  bool(GPIO.input(self.pin))
