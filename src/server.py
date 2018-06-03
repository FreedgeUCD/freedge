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
"""Freedge, a communinty fridge, has multiple sensors to enable users effortlessly 
and immediately know what food is curently available through a web app.

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
"""
import sys
import time
import argparse

from sensors import MagneticSwitch, WeatherAM2315



# #######################
# Hardware Configuration
# #######################
# Define how sensors are connected to Freedge. Raspberry Pi 3 has over
# 40 GPIO PINs, 4 USB ports. The below config. shows how each component 
# is connected (or wired) to the Rasp Pi 3.

# Reference:
# ---------
# Rasp Pi 3B GPIO Pinout:
# Ref: http://pi4j.com/pins/model-3b-rev1.html


# Door Sensor Signal is received from PIN 18 (In BCM Mode). 
# Also, the ground (Black) wire is connected to PIN 4.
GPIO_DOOR_PIN = 18

# Weather sensor use I2C protocol, we follow this tutorial to determine 
# the AM2315 address mapping on Linux: 
# [1] https://shop.switchdoc.com/products/am2315-encased-i2c-temperature-humidity-sensor-for-raspberry-pi-arduino
I2C_AM2315_ADDRESS = 0x5c

def main(args):
  # ##########################
  # Initialize Freedge Cloud
  # ##########################
  INFLUXDB_HOST = 'http://172.30.67.178'
  INFLUXDB_NAME = 'temperature_db'

  # ##########################
  # Initialize Freedge Sensors 
  # ##########################
  door = MagneticSwitch(
      pin=GPIO_DOOR_PIN, 
      id='door_{}'.format(args.device_id))

  environment = WeatherAM2315(
      address=I2C_AM2315_ADDRESS, 
      id='environment_{}'.format(args.device_id))

  print('Initualization Completed. Starting Main loop...')
  # #########################
  # Main Loop 
  # #########################
  # Whenever some one opens the door, is_triggered is set to True 
  # until the door is closed.
  is_triggered = False
  update_interval = 60
  # Start connecting to Google Cloud Server
  while True:       
      if door.is_open() and not is_triggered: 
        print("Door is opening.")
        is_triggered = True
        
      elif door.is_recently_closed() and is_triggered:
        print("Door is closed.")
        time.sleep(1)
        print("\n------------------------")
        print("Retrieving sensor data..")
        print("------------------------\n")
        environment.sense()
        environment.upload()
        print("------------------------\n")
        is_triggered = False
      time.sleep(0.1)


def parse_args():
  args = argparse.ArgumentParser()
  args.add_argument('--device_id',  type=str, default='freedgePrototype')
  return args.parse_args()


if __name__ == '__main__':
  args = parse_args()
  main(args)

  # try: 
  # except KeyboardInterrupt as exit_signal:
  #   print('Ctrl + C is pressed. Cleaning up..')
  #   # door.cleanup()
  # except Exception as e: 
  #   print(e)  # all other expcetions display here

  # Setup some constants with InfluxDB 
  # Host and Database name.
