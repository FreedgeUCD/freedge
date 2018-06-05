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
from sensors import MagneticSwitch, WeatherAM2315, LightStrip, CameraMananger

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

# PIN to receive Door (RED) Signal.
# Also, the ground (BLACK) wire is connected to PIN 4.
GPIO_DOOR_PIN = 14  # in BCM Mode

# Weather sensor (AM2315) uses I2C protocol, we follow this tutorial to determine 
# the  address mapping on Linux: 
# [1] https://shop.switchdoc.com/products/am2315-encased-i2c-temperature-humidity-sensor-for-raspberry-pi-arduino
I2C_AM2315_ADDRESS = 0x5c



class Freedge(object):
  """Freedge, a communinty fridge, has multiple sensors to enable users effortlessly 
  and immediately know what food is curently available through a web app.

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
  def __init__(self, device_id, camera_update_interval, weather_update_interval, verbose):
    """Initialize Freedge object:

    Args:
      device_id: - str - a unique device identifer
      camera_update_interval: - int - update interval for cameras
      weather_update_interval: - int - update interval for weather sensor
      verbose: display debug message
    """
    
    # Camera manager controls a list of camera devices (e.g [0, 1, 2]),
    # handle to take photos whenever there is a trigger event (e.g. door opens) 
    self.camera = CameraMananger(devices=[0, 1, 2], id='%s_cameramanager'%device_id)

    # Magnetic switch sensor senses whenever someone open/close the door.
    self.door = MagneticSwitch(pin=GPIO_DOOR_PIN, id='%s_door'% device_id)

    # WeatherAM2315 senses the current temperature / humidty in Freedge.
    self.environment = WeatherAM2315(address=I2C_AM2315_ADDRESS, id='%s_environment'% device_id)

    # LightStrip controls the LEDs strip in Freedge.
    self.lighting = LightStrip()

    # Determine when to obtain sensory data
    self.is_triggered = False

    # For sending data updates to the cloud in interval.
    self.last_weather_update = time.time()
    self.last_camera_update = time.time()
    self.camera_update_interval = camera_update_interval
    self.weather_update_interval = weather_update_interval

    # For print debugging message to std
    self.verbose = verbose

  def run(self):
    """This function get called in a while-loop 
    to determine the current status of Freedge.
    """

    if self.door.is_open() and not self.is_triggered: 
      if self.verbose:
        print("Door is opening.")
      self.is_triggered = True
      return None

    elif self.is_triggered and self.door.is_recently_closed():
      if self.verbose:
        print("Door is closed.\n")

      # Obtaining Data
      self.lighting.flash()
      time.sleep(2.0)

      data = self.retreive_sensor_data()
      time.sleep(2.0)
      self.lighting.turn_off()
      time.sleep(2.0)

      # Reset update interval states
      self.is_triggered = False
      self.last_camera_update = time.time()
      self.last_weather_update = time.time()

      return data

    else:
      data = {}
      if time.time() - self.last_weather_update > self.weather_update_interval:
        self.last_weather_update = time.time()
        temperature, humidity, ok = self.environment.sense()
        if self.verbose:
          print("===============================")
          print("Retrieving sensor data.")
          print("===============================")
          print('Humidty: {:.2f}%'.format(humidity))
          print('Temperature: {:.2f}*C'.format(temperature))
          print("===============================\n")
        data['environment'] = {
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
    images = self.camera.trigger()

    data = {
      'active_period': {'value': active_period},
      'environment': 
        {'temperature': temperature,
          'humidity': humidity},
      'images': {  # a list of images  data
        'camera0': float('-1'),
        'camera2': float('-1'),
        'camera3': float('-1')},  
    }
    if self.verbose:
      print("===============================")
      print("Retrieving sensor data.")
      print("===============================")
      print('Humidty: {:.2f}%'.format(humidity))
      print('Temperature: {:.2f}*C'.format(temperature))
      print('Active period: {:.2f} second(s)'.format(active_period))
      print("===============================\n")
    return data

  def shutdown(self):
    # Turn off lighting
    self.lighting.turn_off()
    time.sleep(1.0)  # Wating for all the LEDs to turn off.
    # Turn off GPIO
    self.door.cleanup()