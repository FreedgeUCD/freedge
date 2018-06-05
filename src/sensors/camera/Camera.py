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
        # Hack: flip upside down
        image = cv2.flip(image, 1)
        img_file = '/tmp/camera%s.jpg' % self.device
        cv2.imwrite(img_file, image)
        cam.release()
        return image