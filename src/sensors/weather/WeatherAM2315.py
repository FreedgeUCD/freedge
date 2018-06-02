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
    def __init__(self, address, i2c_port="/dev/i2c-1", **kwargs):
        super(WeatherAM2315, self).__init__(**kwargs)
        self.temperature = 0
        self.humidity = -1
        self.good_singal = False
        self.am2315 = AM2315(address, i2c_port)

    def sense(self):
        self.temperature, self.humidity, self.good_singal = self.am2315.sense()
        if ok == 1:
            print("Temperature: {:.2f}*C".format(temperature))
            print("Humidity: {:.2f}%".format(humidity))
        return self
        
    def upload(self):
        if self.cloud_provider:
            data = self.temperature
            self.cloud_provider.upload(data)

