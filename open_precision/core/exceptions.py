class SensorNotConnectedError(Exception):
    """raised when trying to access a sensor that is not connected"""

    def __init__(self, sensor):
        self.sensor = sensor

    def __str__(self):
        return str(self.sensor) + 'is not connected'
