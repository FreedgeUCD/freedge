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
import sys
import time
import argparse

# from cloud.api import AWS
from sensors import CameraMananger, MagneticSwitch, WeatherAM2315

I2C_ADDRESS = 0x5c
GPIO_DOOR_PIN = 18
CAMERAS = [0, 1]

def main(args):
  # TODO: add cloud intergration

  # ###################
  # Initialize Sensors 
  # ####################
  door = MagneticSwitch(
      pin=GPIO_DOOR_PIN, 
      id='door_{}_{}'.format(args.registry_id, args.device_id))
  weather = WeatherAM2315(
      address=I2C_ADDRESS, 
      id='weather_{}_{}'.format(args.registry_id, args.device_id))
  cam_manager = CameraMananger(
      devices=CAMERAS, 
      id='cammanager_{}_{}'.format(args.registry_id, args.device_id))

  # Whenever some one opens the door, 
  # is_triggered is set to True until 
  # the door is closed.
  is_triggered = False

  # ##########
  # Main Loop 
  # ##########
  while True:       
    if door.is_open() and not is_triggered: 
      print("Door is opening.")
      is_triggered = True

    elif door.is_recently_closed():
      print("\nDoor is closed.\n\n")
      time.sleep(1)
      weather.check()
      # cam_manager.trigger()
      is_triggered = False

    time.sleep(0.1)

def parse_args():
  args = argparse.ArgumentParser()
  args.add_argument('--demo_mode',  type=bool, default=False)
  args.add_argument('--project_id', type=str, default='freedge-demo')
  args.add_argument('--location',   type=str, default='us-central1')
  args.add_argument('--registry_id',type=str, default='freedge.org')
  args.add_argument('--device_id',  type=str, default='freedgePrototype')
  args.add_argument('--private_key',type=str, default=None)
  return args.parse_args()
  

if __name__ == '__main__':
  args = parse_args()
  try:  
    main(args)
  except KeyboardInterrupt:
    print('Cleaning up')
    door.cleanup()
  finally:
    sys.exit(0)