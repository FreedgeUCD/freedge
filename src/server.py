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

# from clouds import CloudDB, CloudML
from Freedge import Freedge

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
  # INFLUXDB_HOST = 'http://172.30.67.178'
  # INFLUXDB_NAME = 'temperature_db'
  freedge = Freedge(
      device_id=args.device_id,
      camera_update_interval=args.camera_update_interval,
      weather_update_interval=args.weather_update_interval,
      verbose=True)

  # ##########################
  # Main Loop
  # ##########################
  while True:
    updates = freedge.run()
    if updates:
      print(updates)
      
    time.sleep(0.1)



if __name__ == '__main__':
  args = parse_args()
  main(args)

  # try: 
  # except KeyboardInterrupt as exit_signal:
  #   print('Ctrl + C is pressed. Cleaning up..')
  #   # door.cleanup()
  # except Exception as e: 
  #   print(e)  # all other expcetions display here
