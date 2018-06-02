# MIT License
#
# Copyright (c) 2018 Freedge.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================
"""Freedge, a communinty fridge, has multiple sensors to help users easily 
know what food is curently available.

-------------
Hardware Info
-------------
In this protoype, Freedge would have the following sensors:
   * A Door sensor (Magnetic Switch): to know when someone is using Freedge.
   * A Weather sensor (AM2315): to know the current temperature/humidity.
   * 3 Cameras (ELP 170* Wide angle USB cam): to know what is currently inside
        Freedge.

In addition, we use a Raspberry Pi 3B to act as mailman that sends all the 
sensor data to the Google Cloud IoT Core.

-----------------
How Freedge works
-----------------
  * For every 30 seconds, we collect the current temperature / humidty of the
  freedge.
  * For every 5 minutes,  we collect images inside the freedge 
  (for quality control analysis later).
  * Whenever someone open/close the door, we also collect sensor data.
  * All collected data will be (hopefully safely) stored in Google Cloud.
  
Future Directions:
------------------
  1. How can we improve Freedge to improve customer retention rate?
"""
import sys
import time
import argparse

from cloud.api import GoogleIoTCore
from sensors import CameraMananger, MagneticSwitch, WeatherAM2315

I2C_ADDRESS = 0x5c
GPIO_DOOR_PIN = 18
CAMERAS = [0, 1]

def main(args):

  # ##########################
  # Initialize IoT Cloud
  # ##########################


  # ##########################
  # Initialize Sensors 
  # ##########################
  door = MagneticSwitch(
      pin=GPIO_DOOR_PIN, 
      cloud_provider=iot_cloud,
      id='door_{}_{}'.format(args.registry_id, args.device_id))

  weather_sensor = WeatherAM2315(
      address=I2C_ADDRESS, 
      cloud_provider=iot_cloud,
      id='weather_{}_{}'.format(args.registry_id, args.device_id))

  # cam_manager = CameraMananger(
  #     devices=CAMERAS, 
  #     id='cammanager_{}_{}'.format(args.registry_id, args.device_id),
  #     cloud_provider=iot_cloud)

  # #########################
  #        Main Loop 
  # #########################
  # Whenever some one opens the door, 
  # is_triggered is set to True until 
  # the door is closed.
  is_triggered = False
  try: 
    while True:       
      if door.is_open() and not is_triggered: 
        print("Door is opening.")
        is_triggered = True
      elif door.is_recently_closed():
        print("Door is closed.")
        time.sleep(1)
        print("\n------------------------")
        print("Retrieving sensor data..")
        print("------------------------\n")
        weather_sensor.sense()
        # cam_manager.trigger()
        print("------------------------\n")
        is_triggered = False
      time.sleep(0.1)

  # When someone is pressed Ctrl + C
  except Exception as e:
    print(e)
    print('Cleaning up')
    door.cleanup()
    iot_cloud.disconnect()
  finally:
    sys.exit(0)

def parse_args():
  args = argparse.ArgumentParser()
  args.add_argument('--credential_file',  type=str, help='path to credential json key for inserting data')

  return args.parse_args()
  

if __name__ == '__main__':
  args = parse_args()
  main(args)
