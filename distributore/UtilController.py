from Constants import WEST, SOUTH, NORTH, EAST
from Logger import Logger

#Classe utilizzata per l'approssimazione degli angoli
class UtilController:

    def approximateAngle(self, degree):
            if (350.0 < degree < 360.0 or 0.0 < degree < 10.0):
                return NORTH
            elif (260.0 < degree < 280.0):
                return EAST
            elif (80.0 < degree < 100.0):
                return WEST
            elif (170.5 < degree < 190.0):
                return SOUTH
            else:
                return int(degree)

    def checkDegrees(self, degree):
        if (degree >= 360.0):
            return degree - 360.0
        elif (degree <= 0):
            return degree + 360.0
        else:
            return degree

    def checkAndApproximateAngle(self, degree):
        degreeChecked = self.checkDegrees(degree)
        return self.approximateAngle(degreeChecked)