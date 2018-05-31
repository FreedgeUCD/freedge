# MIT License

# Copyright (c) 2018 Freedge.org

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import argparse

# from cloud.api import AWS
from sensors import CameraMananger, MagneticSwitch, WeatherAM2315

I2C_ADDRESS = 0x5c
GPIO_DOOR_PIN = 18
CAMERAS = [0, 1]

def parse_args():
  args = argparse.ArgumentParser()
  args.add_argument('--demo_mode',  default=False, type=bool)
  args.add_argument('--project_id', default='freedge-demo', type=str)
  args.add_argument('--registry_id',default='freedge.org', type=str)
  args.add_argument('--device_id',  default='freedgePrototype', type=str)
  return args.parse_args()
  
def main(args):
  reg_id = args.registry_id
  dev_id = args.device_id

  # awscloud   = AWS(cloud_api=args.project_id)
  door = MagneticSwitch(
      pin=GPIO_DOOR_PIN, 
      id='door_{}_{}'.format(reg_id, dev_id))
  weather = WeatherAM2315(
      address=I2C_ADDRESS, 
      id='weather_{}_{}'.format(reg_id, dev_id))
  cam_manager = CameraMananger(
      devices=CAMERAS, 
      id='cammanager_{}_{}'.format(reg_id, dev_id))

  while True:       
    if door.is_open() and not cam_manager.is_activated(): 
      print("Door is opening")
      cam_manager.activate() 

    elif not door.is_open() and cam_manager.is_activated():
      print("Door is closed!\nWaiting 1 second...")
      cam_manager.trigger()
      time.sleep(1)
    else:
      print("Door is closed...")
      weather.check()
      cam_manager.trigger()

      time.sleep(1)

    time.sleep(0.1)

if __name__ == '__main__':
  args = parse_args()
  main(args)

# # Clean up when the user exits with keyboard interrupt
# def turnoff(signal, frame):
#   import signal 
#   import sys 
#   sys.exit(0)

# # Cleanup handler for when user hits Ctrl-C to exit
# signal.signal(signal.SIGINT, turnoff) 