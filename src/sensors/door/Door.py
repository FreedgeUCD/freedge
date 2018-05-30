import RPi.GPIO as GPIO
from ..Sensor import Sensor

class Door(Sensor):
    def __init__(port):
        # Rasp Pi 3B GPIO Pinout:
        # Ref: http://pi4j.com/pins/model-3b-rev1.html
        GPIO.setmode(GPIO.BCM)
        PIN_DOOR_SENSOR = 18
        # Set up the door sensor pin.
        # 0 : Close
        # 1 : Open
        GPIO.setup(
        PIN_DOOR_SENSOR, GPIO.IN, 
        pull_up_down = GPIO.PUD_UP) 

    def check():
        door_is_open = GPIO.input(PIN_DOOR_SENSOR) 

    def off():
        GPIO.cleanup() 
