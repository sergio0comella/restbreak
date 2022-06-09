
from math import nan
from Constants import OBS_FOUNDED, TIMESTEP
from Logger import Logger


class ObstaclesAvoidance:
    numDistSensors = 3
    threshold = [800, 800, 800]
    
    def __init__(self, robot):
        self.robot = robot
        self.distanceSensors = [robot.getDevice(
            'distance_sensor_' + str(x)) for x in range(self.numDistSensors)]  # distance sensors
        # Enable all distance sensors
        list(map((lambda s: s.enable(TIMESTEP)), self.distanceSensors))


    def checkObstacles(self):
        distanceSensorsValue = [h.getValue()
                                for h in self.distanceSensors]
        obsFound = [(x < y)
                    for x, y in zip(distanceSensorsValue, self.threshold)]
        if True in obsFound:
            return OBS_FOUNDED
        else:
            return nan
