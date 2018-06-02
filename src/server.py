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

Hardware Info
-------------
In this protoype, Freedge would have the following sensors:
   * A Door sensor (Magnetic Switch): to know when someone is using Freedge.
   * A Weather sensor (AM2315): to know the current temperature/humidity.
   * 3 Cameras (ELP 170* Wide angle USB cam): to know what is currently inside
        Freedge.

In addition, we use a Raspberry Pi 3B to act as mailman that sends all the 
sensor data to the Google Cloud IoT Core.

How it works
------------
  * For every 30 seconds, we collect the current temperature / humidty of the
  fridge as well as the images inside the fridge (for quality control analysis
  later).
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
  iot_cloud = GoogleIoTCore(
      project_id=args.project_id,
      location=args.location,
      registry_id=registry_id,
      device_id=args.device_id,
      private_key=agrs.private_key,
      ca_certs=args.ca_certs,
      encryption_algorithm=args.encryption_algorithm)
  iot_cloud.connect()

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
  except KeyboardInterrupt:
    print('Cleaning up')
    door.cleanup()
    iot_cloud.disconnect()
  finally:
    sys.exit(0)

def parse_args():
  args = argparse.ArgumentParser()
  args.add_argument('--demo_mode',  type=bool, default=False)
  args.add_argument('--project_id', type=str, default='freedge-demo')
  args.add_argument('--location',   type=str, default='us-central1')
  args.add_argument('--registry_id',type=str, default='freedge.org')
  args.add_argument('--device_id',  type=str, default='freedgePrototype')
  args.add_argument('--private_key',type=str, default=None)
  args.add_argument('--ca_certs',type=str, default=None)
  args.add_argument('--encryption_algorithm' choices=('RS256', 'ES256'), default='ES256')

  return args.parse_args()
  

if __name__ == '__main__':
  args = parse_args()
  main(args)
