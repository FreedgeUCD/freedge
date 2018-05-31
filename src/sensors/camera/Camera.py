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

import cv2
from ..Sensor import Sensor

class Camera(Sensor):
    def __init__(self, device=0, **kwargs):
        self.device = device
        super(Camera,self).__init__(**kwargs)

    def takes_photo(self):
        print("\nTaking photo from camera %s"% self.device)
        cam = cv2.VideoCapture(self.device)
        ret, image = cam.read()
        if not ret:
            print('Cannot read camera %s' % self.device)
            cam.release()
            return None
        img_file = '/tmp/camera%s.jpg' % self.device
        cv2.imwrite(img_file, image)
        cam.release()
        return image

class CameraMananger(object):
    def __init__(self, devices, id, cloud_provider=None):
        self.id = id
        self.activated = False
        self.cameras = self._setup(devices, cloud_provider)

    def activate(self):
        self.activated = True

    def is_activated(self):
        return self.activated

    def trigger(self):
        self.activated = False
        for cam in self.cameras:
            cam.takes_photo()


    def _setup(self, devices,cloud_provider):
        cams = []
        _, registry_id, device_id = self.id.split('_')
        for idx, device in enumerate(devices):
            cams.append(
                Camera(device, 
                    id='cam{}_{}_{}'.format(idx, registry_id, device_id),
                    cloud_provider=cloud_provider))

        return cams
#      trigger_cameras = False
#       for cam_id in cameras:
#         print("\nTaking photo from camera %s"%cam_id)
#         cm = cv2.VideoCapture(cam_id)
#         ret, frame = cam.read()

#         if not ret:
#           print('Cannot read camera %s' % id)
#           cam.release()
#           continue

#         img_file = '/home/pi/freedge/src/output/camera%s.jpg'%cam_id
#         cv2.imwrite(img_file, frame)
#         cam.release()

#       print("Photos are taken and sent to server.\n")