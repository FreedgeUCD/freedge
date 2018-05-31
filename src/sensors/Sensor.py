"""Abstract Sensor Object
"""

class Sensor(object):
    def __init__(self, id, cloud_provider=None):
        self.id = id
        self.cloud_provider = cloud_provider

    def connect(self):  
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

        