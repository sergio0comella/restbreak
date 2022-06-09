from Constants import MAP, F, S, C, O, L, W
from Logger import Logger
from Position import Position

          #  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18  19 20
STARTMAP = [[W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],  # 0
            [W, F, F, F, W, F, F, F, F, F, 0, F, F, F, F, F, W, F, F, F, W],  # 1
            [W, F, F, F, W, F, F, F, F, F, L, F, F, F, F, F, W, F, F, F, W],  # 2
            [W, F, F, F, W, F, F, F, F, F, L, F, F, F, F, F, W, F, F, F, W],  # 3
            [W, F, F, F, W, F, C, L, L, L, C, L, L, L, C, F, W, F, F, F, W],  # 4
            [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 5
            [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 6
            [W, F, F, F, 1, L, C, L, L, L, C, L, L, L, C, L, 6, F, F, F, W],  # 7
            [W, W, W, W, W, F, L, F, F, F, L, F, F, F, L, F, W, W, W, W, W],  # 8
            [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 9
            [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 10
            [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 11
            [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 12
            [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 13
            [W, F, F, F, 2, L, C, L, L, L, C, L, L, L, C, L, 5, F, F, F, W],  # 14
            [W, W, W, W, W, F, L, F, F, F, L, F, F, F, L, F, W, W, W, W, W],  # 15
            [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 16
            [W, F, F, F, W, F, L, F, F, F, L, F, F, F, L, F, W, F, F, F, W],  # 17
            [W, F, F, F, 3, L, C, L, L, L, C, L, L, L, C, L, 4, F, F, F, W],  # 18
            [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 19
            [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W]]  # 20


class Map:
    def __init__(self):
        self.MAP = STARTMAP
        
    def resetMap(self):
        self.MAP = MAP

    def getOfficePosition(self, office):
        for i in range(self.getSizeOfMap()[0]):
            for j in range(self.getSizeOfMap()[1]):
                if self.MAP[i][j] == office:
                    return Position(i, j)
        return Position(0, 0)

    def getSizeOfMap(self):
        return [len(MAP), len(MAP[0])]

    def setNewObstacle(self, position):
        x = position.getX()
        y = position.getY()
        if x > 0 and x < self.getSizeOfMap()[0]:
            if y > 0 and y < self.getSizeOfMap()[1]:
                self.MAP[x][y] = O
        Logger.info(f"Obstacle to: ({str(x)}, {str(y)})")
    
    def getMap(self):
        return self.MAP
