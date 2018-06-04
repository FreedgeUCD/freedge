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
"""
-----------------
How Freedge works
-----------------
  * For every 120 seconds, we collect the current temperature / humidty of the
  freedge.

  * For every 600 seconds (10 mins),  we collect images inside the freedge 
  (for quality control analysis later).

  * Whenever someone open/close the door, we also collect data from all
  sensors, including images, temp/hudmidty, and active period.
  
  * In addition, the update interval will be reset starting from last active 
  period.

  * All collected data will send to a Cloud Database.
"""
import sys
import time
import argparse

from Freedge import Freedge
from cloud.CloudDB import CloudDB


def parse_args():
  args = argparse.ArgumentParser()
  args.add_argument('--device_id', type=str, default='freedgePrototype')
  args.add_argument('--camera_update_interval', type=int, default=600)
  args.add_argument('--weather_update_interval', type=int, default=120)
  return args.parse_args()


def main(args):
  # ############################
  # Initialize cloud and Freedge
  # ############################
  cloud = CloudDB(
      host='172.30.67.178', 
      port=8086, 
      database='freedgeDB', 
      verbose=True)

  freedge = Freedge(
      device_id=args.device_id,
      camera_update_interval=args.camera_update_interval,
      weather_update_interval=args.weather_update_interval,
      verbose=True)

  # ##########################
  # Main Loop
  # ##########################
  print('Device is intialized. Starting running...')
  try: 
    while True:
      new_updates = freedge.run()
      if new_updates:
        msg, ok = cloud.upload(new_updates, args.device_id, location='US')
      time.sleep(0.1)
      
  except KeyboardInterrupt as exit_signal:
    print('Ctrl + C is pressed')
    freedge.shutdown()

if __name__ == '__main__':
  args = parse_args()
  main(args)