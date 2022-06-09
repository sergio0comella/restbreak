


class Position:
    def __init__(self, x, y):
        self.setX(x)
        self.setY(y)

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPositionArray(self):
        return (self.getX(), self.getY())

    def printCoordinate(self):
        print("Coordinate X: " + str(self.getX()) +
              " Coordinate Y: " + str(self.getY()))
        
    def comparePosition(self, position):
        return self.x == position.x and self.y == position.y
