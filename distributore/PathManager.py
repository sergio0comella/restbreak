from Astar import Astar
from Compass import Compass
from Constants import MAP
from Astar import Astar
from CustomException import GoalPositionAlreadyReached, GoalPositionNotFound, GoalPositionUnreacheable
from Logger import Logger
from Constants import *
from Map import Map
from PathFollower import PathFollower
from Position import Position
from UtilController import UtilController
from math import nan


class PathManager:

    def __init__(self, robot):
        self.astar = Astar(MAP)
        self.utilController = UtilController()
        self.route = None
        self.pathFollower = PathFollower(robot)
        self.startPosition = Position(SX, SY)
        self.goalPosition = nan
        self.status = START
        self.currentPosition = Position(SX, SY)
        self.directions = None #FIFO
        self.intersections = None #FIFO
        self.clockwise = True
        self.lastDirection = nan
        self.map = Map()
        self.compass = Compass(robot)


    def run(self):
        return self.pathFollower.followPath()

    def resetOverIntersection(self):
        self.pathFollower.resetOverIntersection()

    # dopo le verifiche base
    # calcolo route > intersezioni > direzioni
    def getFastestRoute(self):
        if self.goalPosition == nan:
            raise GoalPositionNotFound('Goal position not found')
        
        if self.checkGoalPosition():
            raise GoalPositionAlreadyReached('Goal position already reached')

        self.route = self.astar.findPath(self.startPosition.getPositionArray(), self.goalPosition)

        if self.route is None:
            raise GoalPositionUnreacheable('Goal position unreacheble')

        self.intersections = self.getIntersectionNodesFromRoute()
        Logger.info(f"Intersections: { self.intersections }")

        self.directions = self.getDirectionsFromIntersections(self.intersections)
        Logger.info(f"Directions: {self.directions}")
        
        return self.directions

    # Dalla mappa verifico se il punto del percorso è un'intersezione e la salvo
    def getIntersectionNodesFromRoute(self):
        intersections = []
        if self.route == None:
            return []

        intersections.append(self.route[0])
        for node in self.route[1:-1]:
            if MAP[node[0]][node[1]] == C:
                intersections.append(node)

        intersections.append(self.route[-1])
        return intersections

    # Dalle intersezioni calcolo gli angoli corrispondenti
    def getDirectionsFromIntersections(self, intersections):
        directions = []

        prevNode = intersections[0]
        for currentNode in intersections[1:]:
            if currentNode[0] > prevNode[0]:
                directions.append(NORTH)
            elif currentNode[0] < prevNode[0]:
                directions.append(SOUTH)
            elif currentNode[1] > prevNode[1]:
                directions.append(WEST)
            elif currentNode[1] < prevNode[1]:
                directions.append(EAST)
            else:
                print("Invalid intersetions")
            prevNode = currentNode

        return directions

    def getGoalPosition(self):
        return self.goalPosition

    def setGoalPosition(self, goalPosition):
        self.goalPosition = goalPosition

    #dall'ufficio numerico prendo le coordinate e le imposto nel goal
    def setGoalPositionFromOfficeNumber(self, officeNumber):
        officePosition = self.map.getOfficePosition(officeNumber).getPositionArray()
        self.setGoalPosition(officePosition)

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def setStartPosition(self, startPosition):
        self.startPosition = startPosition

    #angles
    def popDirection(self):
        return self.directions.pop(0) if self.directions else UNKNOWN

    #landmark
    def popIntersection(self):
        return self.intersections.pop(0) if self.intersections else UNKNOWN

    def getRobotAngle(self):
        return self.utilController.checkDegrees(self.getRobotAngle())

    def getRobotAngleWithoutCheck(self):
        return self.getRobotAngle()

    def getRobotAngleApproximate(self):
        currAngle = self.getRobotAngle()
        return self.utilController.checkAndApproximateAngle(currAngle)

    #Aggiorno la positione corrente del robot con la prima intersezione in coda
    # e verifico se sono arrivato al goal
    def updatePosition(self):
        currIntersect = self.popIntersection()
        self.currentPosition = Position(currIntersect[0], currIntersect[1])
        self.checkGoalPosition()
            
    def checkGoalPosition(self):
        goalPosition = Position(self.goalPosition[0], self.goalPosition[1])
        Logger.debug(f"|_ {self.currentPosition.getPositionArray()} _|")
        if goalPosition.comparePosition(self.currentPosition):
            self.setStatus(GOAL)
            return True
        return False

    def updateClockwise(self, newAngle, currAngle):
        if(newAngle == NORTH):
            if(180 <= currAngle <= 359.9):
                self.clockwise = False
            elif(0.1 <= currAngle < 180):
                self.clockwise = True
        elif(newAngle == SOUTH):
            if(180.1 <= currAngle <= 359.9):
                self.clockwise = True
            elif(0 <= currAngle <= 179.9):
                self.clockwise = False
        elif(newAngle == WEST):
            if(0 <= currAngle <= 89.9 or 269.9 <= currAngle <= 359.9):
                self.clockwise = True
            elif(90 <= currAngle <= 270.1):
                self.clockwise = False
        elif(newAngle == EAST):
            if(90.1 <= currAngle <= 270):
                self.clockwise = True
            elif(270.1 <= currAngle <= 359.9 or 0 <= currAngle <= 89.9):
                self.clockwise = False

    def calculateRotationTime(self, degrees):
        return abs(degrees) / ROTSPEED

    def isClockwise(self):
        return self.clockwise
    
    def goalReached(self):
        Logger.goalReached()
        self.setStatus(START)
        self.setStartPosition(self.currentPosition)
        print("Sblocca il dispositivo, poi inserisci una nuova destinazione:")
        self.map.resetMap()
        
    def uTurn(self):
        approx = self.getRobotAngleApproximate()
        if(approx == NORTH):
            return SOUTH
        elif(approx == SOUTH):
            return NORTH
        elif(approx == EAST):
            return WEST
        elif(approx == WEST):
            return EAST

    def setLastDirection(self, direction):
        self.lastDirection = direction
        
    def getLastDirection(self):
        return self.lastDirection
    
    def updateObstaclesInMap(self):
        orientation = self.getRobotAngleApproximate()
        # prendo la posizione non raggiungibile
        position = self.intersections[0]
        x = position[0]
        y = position[1]
        obstacle = Position(x, y)
        if orientation == NORTH:
            obstacle = Position(x - 2, y)
        if orientation == EAST:
            obstacle = Position(x, y - 2)
        if orientation == SOUTH:
            obstacle = Position(x + 2, y)
        if orientation == WEST:
            obstacle = Position(x, y + 2)

        self.map.setNewObstacle(obstacle)
        self.astar.updateMap(self.map.getMap())
        return obstacle
    
    def getRobotAngle(self):
        return self.compass.compassToDegree()

