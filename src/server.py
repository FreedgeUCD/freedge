import time
import sys
import signal 

from sensors.camera import Camera
from sensors.weather import AM2315
from sensors.door import Door


# Global states
cameras = [0, 1, 2]


# Clean up when the user exits with keyboard interrupt
def turnoff(signal, frame): 
    sys.exit(0)

# Cleanup handler for when user hits Ctrl-C to exit
signal.signal(signal.SIGINT, turnoff) 

def init_camera():
  raise NotImplementedError

if __name__ == '__main__':

  ## Global states ##
  door_is_open = None
  trigger_cameras = False

  ## Init Sensors ##
  cameras = init_camera()
  door_sensor = DoorSwitch()

  while True: 
    if door_is_open and not trigger_cameras: 
      print("Door is opening")
      trigger_cameras = True

    elif not door_is_open and trigger_cameras:  
      print("Door is closed!")
      print("Waiting 2 seconds...")
      time.sleep(2);
      trigger_cameras = False
      for cam_id in cameras:
        print("\nTaking photo from camera %s"%cam_id)
        cam = cv2.VideoCapture(cam_id)
        ret, frame = cam.read()

        if not ret:
          print('Cannot read camera %s' % id)
          cam.release()
          continue

        img_file = '/home/pi/freedge/src/output/camera%s.jpg'%cam_id
        cv2.imwrite(img_file, frame)
        cam.release()

      print("Photos are taken and sent to server.\n")

    time.sleep(0.1)
