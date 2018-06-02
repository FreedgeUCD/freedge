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

from ..Sensor import Sensor
from tentacle_pi.AM2315 import AM2315

class WeatherAM2315(Sensor):
    """"AM2315 sensor measures temperature and humidity 
    in the environment.
    """
    def __init__(self, address, **kwargs):
        super(WeatherAM2315, self).__init__(**kwargs)
        self.am2315 = AM2315(address, "/dev/i2c-1")

    def check(self):
        temperature, humidity, ok = self.am2315.sense()
        # if ok == 1:
        print("Temperature: {:.2f}*C".format(temperature))
        print("Humidity: {:.2f}%".format(humidity))
        
