
from Constants import TIMESTEP


class GroundSensor:
    
    def __init__(self, robot, sensorName):  
        self.sensor = robot.getDevice(sensorName)
        self.sensor.enable(TIMESTEP)

    def getValue(self):
        return self.sensor.getValue()
