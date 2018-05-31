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

import RPi.GPIO as GPIO
from ..Sensor import Sensor

class MagneticSwitch(Sensor):
    def __init__(self,  pin, **kwargs):
        self.pin = pin
        super(MagneticSwitch, self).__init__(**kwargs)
        
        # Rasp Pi 3B GPIO Pinout:
        # Ref: http://pi4j.com/pins/model-3b-rev1.html
        GPIO.setmode(GPIO.BCM)

        # Set up the door sensor pin.
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

    def is_open(self):
        # 0 : Close // 1 : Open
        return  bool(GPIO.input(self.pin))
