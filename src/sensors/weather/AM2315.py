from ..Sensor import Sensor
from tentacle_pi.AM2315 import AM2315

class WeatherAM2315(Sensor):
    """"
    This sensor measures temperature and humidity 
    in the environment.
    """
    def __init__(self, address, **kwargs):
        super(WeatherAM2315, self).__init__(**kwargs)
        self.am2315 = AM2315(address,"/dev/i2c-1")

    def check(self):
        temperature, humidity, ok = self.am2315.sense()
        if ok == 1:
            print("Temperature: {:.2f}*C".format(temperature))
            print("Humidity: {:.2f}%".format(humidity))
            
