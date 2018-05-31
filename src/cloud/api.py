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

import json
import base64
import requests
import datetime

class CloudAPI(object):
  """Abstract Class for Cloud API integration.

  It enables us to (potentially) use Google Cloud, MS Azure, or AWS service
  in a unifed way.
  """
  def __init__():
    self.connected = False

  def is_connected():
    return self.connected

  def upload(self, endpoint_url, jwt, b64_buf):
    headers = {
      "Authorization": "Bearer {}".format(jwt),
      "Content-Type" : "application/json",
      "Cache-Control": "no-cache"}
    res = requests.post(
        endpoint_url, 
        headers=headers,
        data=json.dumps({"binaryData": b64_buf}).encode("utf-8"))
    print("POST HTTP Code={}".format(res.status_code))

    # @TODO: cache failed upload images.
    if res.status_code != 200:
        print(res.json())
        filename = time.strftime("/tmp/failure_image_%Y%M%d_%H%M%S.jpg")
        with open(filename, "wb") as f:
            f.write(base64.urlsafe_b64decode(b64_buf))
        print("Saved failed image to {}".format(filename))


 
class Google(CloudAPI):
  # google_cloud_url = "https://cloudiotdevice.googleapis.com/v1/projects/{}/locations/{}/registries/{}/devices/{}:publishEvent".format(
  #   args.project_id, args.location, args.registry_id, args.device_id)
  def __init__(cloud_api, **kwargs):
    self.cloud_api = cloud_api
    super(Google, self).__init__(**kwargs)
    raise NotImplementedError

  def upload(data):
      raise NotImplementedError


class AWS(CloudAPI):
  def __init__(cloud_api, **kwargs):
    raise NotImplementedError

  def upload(data):
    raise NotImplementedError