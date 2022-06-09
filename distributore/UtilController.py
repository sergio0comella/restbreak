from Constants import WEST, SOUTH, NORTH, EAST
from Logger import Logger

class UtilController:
    def stringFromCoord(coordinates):
        if coordinates != False:
            return "("+str(coordinates[0])+", "+str(coordinates[1])+")"
        else:
            return ""


    def stringFromOrientation(orientation):
        if orientation == WEST:
            return "WEST"
        elif orientation == EAST:
            return "EAST"
        elif orientation == NORTH:
            return "NORTH"
        elif orientation == SOUTH:
            return "SOUTH"
        else:
            return ""

    def approximateAngle(self, degree):
            if (355.0 < degree < 360.0 or 0.0 < degree < 5.0):
                return NORTH
            elif (265.0 < degree < 275.0):
                return EAST
            elif (85.0 < degree < 95.0):
                return WEST
            elif (175.5 < degree < 185.0):
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