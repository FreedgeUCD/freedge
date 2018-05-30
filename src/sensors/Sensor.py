"""Abstract Sensor Object
"""

class Sensor(object):
    def __init__(port):
        self.port = port

    def connect():
        raise NotImplementedError

    def disconnect():
        raise NotImplementedError

        