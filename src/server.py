import time
import sys
import signal 
import PIL
import cv2
import RPi.GPIO as GPIO

# Set Broadcom mode so we can address GPIO 
# pins by number.
# Ref:
#  Rasp Pi 3B Pinout:
#  http://pi4j.com/pins/model-3b-rev1.html
GPIO.setmode(GPIO.BCM) 
PIN_DOOR_SENSOR = 18

# Set up the door sensor pin.
# 0 : Close
# 1 : Open
GPIO.setup(
  PIN_DOOR_SENSOR, GPIO.IN, 
  pull_up_down = GPIO.PUD_UP) 

# Clean up when the user exits with keyboard interrupt
def turnoff(signal, frame): 
    GPIO.cleanup() 
    sys.exit(0)

# Get all available cameras

# Global states
cameras = [0, 1, 2]
door_is_open = None
trigger_cameras = False

# Cleanup handler for when user hits Ctrl-C to exit
signal.signal(signal.SIGINT, turnoff) 
while True: 
  door_is_open = GPIO.input(PIN_DOOR_SENSOR) 
  if door_is_open and not trigger_cameras: 
    print("Door is opening")
    trigger_cameras = True
  elif not door_is_open and trigger_cameras:  
    print("Door is closed!")
    print("Waiting 2 seconds...")
    time.sleep(2);
    for cam_id in cameras:
      print("\nTaking photo from camera %s"%cam_id)
      cam = cv2.VideoCapture(cam_id)
      ret, frame = cam.read()
      if not ret:
        print('Cannot read camera %s' % id)
        cam.release()
        continue
      cv2.imwrite('./output/camera%s.jpg'%cam_id, frame)
      cam.release()
    print("Photos are taken and sent to server.\n")
    trigger_cameras = False

  time.sleep(0.1)
