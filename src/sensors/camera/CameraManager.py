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
# =============================================================================
"""Camera Manager allows program to control activate multiple cameras
at the same time.
"""
from .Camera import Camera

class CameraMananger(object):
    def __init__(self, devices, id, cloud_provider=None):
        self.id = id
        self.activated = False
        self.manager = self._setup(devices, cloud_provider)

    def activate(self):
        self.activated = True

    def is_activated(self):
        return self.activated

    def trigger(self):
        self.activated = False
        for cam in self.manager:
            cam.takes_photo()

    def _setup(self, devices,cloud_provider):
        manager = []
        _, registry_id, device_id = self.id.split('_')
        for idx, device in enumerate(devices):
            camera = Camera(
                device=device, 
                id='cam{}_{}_{}'.format(idx, registry_id, device_id), 
                cloud_provider=cloud_provider)
            manager.append(camera)
        return manager