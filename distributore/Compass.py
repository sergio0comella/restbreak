import math

from Constants import TIMESTEP
class Compass:
    def __init__(self, robot):
        self.compass_xy = robot.getDevice('compass')
        self.compass_xy.enable(1)

    def getCompass(self):
        self.compassXY = self.compass_xy.getValues()
        return [self.compassXY[0], self.compassXY[1], self.compassXY[2]]

    def compassToDegree(self):
        north = self.getCompass()
        rad = (math.atan2(north[0], north[2]))
        bearing = ((rad - 1.5708) / math.pi) * 180.0
        if(bearing <= 0):
            bearing += 360.0
        return round(float(bearing), 2)
