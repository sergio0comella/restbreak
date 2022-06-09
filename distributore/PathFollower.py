from Constants import OBS_FOUNDED, CROSS, GO_DX, GO_SX

from Logger import Logger
from GroundSensor import GroundSensor
from Compass import Compass
import math

from ObstaclesAvoidance import ObstaclesAvoidance


class PathFollower:

    def __init__(self, robot):
        self.robot = robot
        self.isLineLost = False
       
        self.intersectionSensorFirst = GroundSensor(self.robot, 'ir_int0')
        self.intersectionSensorSecond = GroundSensor(self.robot, 'ir_int1')
        self.leftSensor = GroundSensor(self.robot, 'ir0')
        self.rightSensor = GroundSensor(self.robot, 'ir1')

        self.isOverIntersection = False
        
        self.obstaclesAvoidance = ObstaclesAvoidance(self.robot)
        
        
    def isRedPath(self):
        return int(self.intersectionSensorFirst.getValue()) < 10 or int(self.intersectionSensorSecond.getValue() < 10)
    
    def followPath(self):
        leftSensorValue = int(self.leftSensor.getValue())
        rightSensorValue = int(self.rightSensor.getValue())
        
        obstaclesCheck = self.obstaclesAvoidance.checkObstacles()
        if obstaclesCheck == OBS_FOUNDED:
            return OBS_FOUNDED
          
        #Se sono già in un intersezione non invio altre letture di "CROSS"
        if self.isOverIntersection:
            self.isOverIntersection = self.isRedPath()
            return
        
        if self.isRedPath():
            self.isOverIntersection = True
            return CROSS
        elif (leftSensorValue > rightSensorValue) and (4 < leftSensorValue < 16):
            return GO_SX
        elif (rightSensorValue > leftSensorValue) and (4 < rightSensorValue < 16):
            return GO_DX
        
        return

    def resetOverIntersection(self):
        self.isOverIntersection = False
