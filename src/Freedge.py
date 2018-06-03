
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
import time
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

# Weather sensor (AM2315) uses I2C protocol, we follow this tutorial to determine 
# the  address mapping on Linux: 
# [1] https://shop.switchdoc.com/products/am2315-encased-i2c-temperature-humidity-sensor-for-raspberry-pi-arduino
I2C_AM2315_ADDRESS = 0x5c

class Freedge(object):
  """Freedge, a communinty fridge, has multiple sensors to enable users effortlessly 
  and immediately know what food is curently available through a web app.
  -----------------
  How Freedge works
  -----------------
  * For every `weather_update_interval` seconds, we collect the current 
  temperature / humidty of freedge.

  * For every `camera_update_interval` seconds,  we collect images inside the 
  freedge (for quality control analysis later).

  * Whenever someone open/close the door, we also collect data from all
  sensors, including images, temp/hudmidty, and active period. In addition,
  the update interval will be reset starting from last active period.

  * All collected data will send to a Cloud Database.

  -------------
  Hardware Info
  -------------
  In this protoype, Freedge would have the following sensors:
    * A Door sensor (Magnetic Switch): to know when someone is using Freedge.
    * A Weather sensor (AM2315): to know the current temperature/humidity.
    * 3 Cameras (ELP 170* Wide angle USB cam): to know what is currently inside
          Freedge.

  In addition, we use a Raspberry Pi 3B to act as mailman that sends all the 
  sensor data to cloud.
  """
  def __init__(device_id, camera_update_interval, weather_update_interval, verbose):
    """Initialize Freedge object:

    Args:
      device_id: - str - a unique device identifer
      camera_update_interval: - int - update interval for cameras
      weather_update_interval: - int - update interval for weather sensor
      verbose: display debug message
    """
    self.is_triggered = False
    self.last_weather_update = 0
    self.last_camera_update = 0
    self.camera_update_interval = camera_update_interval
    self.weather_update_interval = weather_update_interval
    self.verbose = verbose

    self.door = MagneticSwitch(
        pin=GPIO_DOOR_PIN, 
        id='%s_door'% device_id)
    self.environment = WeatherAM2315(
        address=I2C_AM2315_ADDRESS, 
        id='%s_environment'% device_id)


  def run(self, verbose=True):
    if self.door.is_open() and not self.is_triggered: 
      if verbose:
        print("Door is opening.")
      self.is_triggered = True
      return None

    elif self.is_triggered and self.door.is_recently_closed():
      if verbose:
        print("Door is closed.\n")
      time.sleep(1)
      self.is_triggered = False
      self.last_camera_update = time.time()
      self.last_weather_update = time.time()
      return self.retreive_sensor_data()

    else:
      data = {}
      if time.time() - self.last_weather_update > self.weather_update_interval:
        temperature, humidity, ok = self.environment.sense()
        if verbose:
          print('Temperature: {:.2f}*C'.format(temperature))
          print('Humidty: {:.2f}*C'.format(humidity))
        self.last_weather_update = time.time()
        data['evironment'] = {
          'temperature': temperature,
          'humidity': humidity
        }
      return data

  def retreive_sensor_data(self):
    # Obtain temperature, humidty data
    temperature, humidity, ok = self.environment.sense()
    # Obtain time duration that user
    # opens and closes the door.
    active_period = self.door.get_active_period()
    data = {
      'active_period': active_period,
      'environment': 
        {'temperature': temperature,
          'humidity': humidity},
      'images': None,  # a list of images  data
    }
    if verbose:
      print("-----------------------")
      print("Retrieving sensor data.")
      print("------------------------\n")
      print('Active period: {:.2f}'.format(active_period))
      print('Temperature: {:.2f}*C'.format(temperature))
      print('Humidty: {:.2f}*C'.format(humidity))
      print("-----------------------\n")

    return data