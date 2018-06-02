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
import json
import base64
import requests
import datetime
from .utils import create_jwt

class CloudAPI(object):
  """Abstract Class for Cloud API integration.

  It enables us to (potentially) use Google Cloud, MS Azure, or AWS service
  in a unifed way.
  """
  def __init__(self, private_key, encryption_algorithm, ca_certs):
      self.connected = False
      self.ca_certs = ca_certs
      self.private_key = private_key
      self.algorithm = encryption_algorithm
      self.connected = False

  def is_connected(self):
    return self.connected

  def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
      """Callback for when a device connects."""
      print('Connection Result:', error_str(rc))
      self.connected = True

  def on_disconnect(self, unused_client, unused_userdata, rc):
      """Paho callback for when a device disconnects."""
      print('Disconnected:', error_str(rc))
      self.connected = False

  def on_publish(self, unused_client, unused_userdata, unused_mid):
      """Paho callback when a message is sent to the broker."""
      print('on_publish')

  def on_message(self, unused_client, unused_userdata, message):
      """Callback when the device receives a message on a subscription."""
      payload = str(message.payload)
      print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
              payload, message.topic, str(message.qos)))

      # The device will receive its latest config when it subscribes to the
      # config topic. If there is no configuration for the device, the device
      # will receive a config with an empty payload.
      if not payload:
          return

      # The config is passed in the payload of the message. In this example,
      # the server sends a serialized JSON string.
      data = json.loads(payload)
      return data

  def wait_for_connection(self, timeout):
      """Wait for the device to become connected."""
      total_time = 0
      while not self.connected and total_time < timeout:
          time.sleep(1)
          total_time += 1
      if not self.connected:
          raise RuntimeError('Could not connect to MQTT bridge.')


class GoogleIoTCore(CloudAPI):
  """Google Cloud IoT Core API
  """
  def __init__(self, project_id, cloud_region, registry_id, device_id, **kwargs):
    self.http_base_url = "https://cloudiotdevice.googleapis.com/v1"
    self.mqtt_bridge_hostname = "http://mqtt.googleapis.com"
    self.mqtt_bridge_port = 8883
    self.project_id = project_id
    self.cloud_region = cloud_region
    self.registry_id = registry_id
    self.device_id = device_id

    self.mqtt_client = None
    super(Google, self).__init__(**kwargs)

  def mqtt_upload(self, encoded_json_data):
      mqtt_telemetry_topic = '/devices/{}/events'.format(self.device_id)
      self.mqtt_client.publish(mqtt_telemetry_topic, encoded_data, qos=1)


  def connect(self, ca_certs):
    self.mqtt_client = self.establish_mqtt_connection(ca_certs)
    self.connected = True

  def disconnect(self):
    self.mqtt_client.disconnect()
    self.mqtt_client.loop_stop()

  def establish_mqtt_connection(self, ca_certs, mqtt_bridge_hostname, mqtt_bridge_port):
      """Create our MQTT client. The client_id is a unique string that identifies
      this device. For Google Cloud IoT Core, it must be in the format below."""
      
      client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
          project_id, 
          cloud_region, 
          registry_id, 
          device_id)
      client = mqtt.Client(client_id=client_id)
      # With Google Cloud IoT Core, the username field is ignored, and the
      # password field is used to transmit a JWT to authorize the device.
      json_web_token = create_jwt(
          project_id=self.project_id,
          private_key_file=self.private_key,
          algorithm=self.algorithm)
      client.username_pw_set(username='unused', password=json_web_token))

      # Enable SSL/TLS support.
      client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

      # Register message callbacks. https://eclipse.org/paho/clients/python/docs/
      # describes additional callbacks that Paho supports. In this example, the
      # callbacks just print to standard out.
      client.on_connect = self.on_connect
      client.on_publish = self.on_publish
      client.on_disconnect = self.on_disconnect
      client.on_message = self.on_message

      # Connect to the Google MQTT bridge.
      client.connect(mqtt_bridge_hostname, mqtt_bridge_port)
      client.loop_start()

      return client

  def http_upload(self, encoded_data):
      raise NotImplementedError


def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))

