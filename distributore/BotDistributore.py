
from Position import Position
from controller import Robot
from numpy import isfortran
from CustomException import GoalPositionAlreadyReached, GoalPositionNotFound, GoalPositionUnreacheable
from PathManager import PathManager
from Constants import *
from Logger import Logger
from UtilController import UtilController
from WheelMotor import WheelMotor
from KeyboardController import KeyboardController
from Map import Map

import time
import numpy as np


class BotDistributore:

    def __init__(self):
        self.utilController = UtilController()
        self.robot = Robot()
        self.robot.step(int(self.robot.getBasicTimeStep()))
        self.leftMotor = WheelMotor(self.robot, 'left wheel motor')
        self.rightMotor = WheelMotor(self.robot, 'right wheel motor')

        self.isRotating = False

        self.pathManager = PathManager(self.robot)
        self.keyboardController = KeyboardController(self.robot)
        self.isStarted = True
        self.waitingBeforeCA = True
        self.isCollisionAvoidance = False

    def run(self):
        print("In quale ufficio devo recarmi? ")
        while self.robot.step(TIMESTEP) != -1:
            if not self.keyboardController.canRun() and self.isWaitingCommand():
                self.keyboardController.update()
                continue
            
            if self.pathManager.getStatus() == START:
                self.pathManager.setStatus(INSERT)

            elif self.pathManager.getStatus() == INSERT:
                Logger.info(f"Ufficio inserito: {self.keyboardController.getOffice()}")
                officeNumber = self.keyboardController.getOffice()
                self.pathManager.setGoalPositionFromOfficeNumber(officeNumber)
                self.pathManager.setStatus(COMPUTING)

            elif self.pathManager.getStatus() == COMPUTING:
                if not self.pathManager.checkGoalPosition():
                    try:
                        self.pathManager.getFastestRoute()
                        self.pathManager.setStatus(RUN)
                    except (GoalPositionNotFound, GoalPositionUnreacheable) as error:
                        Logger.info(f"{error} --> Ritorno alla base")
                        self.pathManager.setGoalPosition(Position(SX, SY).getPositionArray())
                    except GoalPositionAlreadyReached as reached:
                        Logger.info(f"{reached}")

            elif self.pathManager.getStatus() == RUN:
                pathStatus = self.pathManager.run()
                
                #Attendo prima 5 secondi
                if pathStatus == OBS_FOUNDED and self.waitingBeforeCA:
                    self.waitingBeforeCA = False
                    self.stopMoving()
                    self.stepRotation(self.robot.getTime() + TIME_BEFORE_CA)
                    self.setWheelsSpeed(SPEED, SPEED)
                    continue
                else:
                    self.waitingBeforeCA = True

                # al primo step verifico la prima direzione calcolata
                if self.isStarted and not self.isCollisionAvoidance:
                    self.handleCross()
                    self.isStarted = False
                elif self.isCollisionAvoidance and pathStatus == CROSS:
                    self.isCollisionAvoidance = False
                    self.stopMoving()
                    self.isStarted = True

                self.managePathStatus(pathStatus)

            elif self.pathManager.getStatus() == GOAL:
                self.goalReached()
                self.isStarted = True
                self.keyboardController.reset()
                self.pathManager.goalReached()
                self.keyboardController.lockStatus()

    # Lo stato del robot è START 
    def isWaitingCommand(self):
        return self.pathManager.getStatus() == START

    def stopMoving(self):
        self.setWheelsSpeed(0, 0)

    def setWheelsSpeed(self, left, right):
        self.leftMotor.setMotorSpeed(left)
        self.rightMotor.setMotorSpeed(right)

    def turnLeft(self):
        self.setWheelsSpeed(SPEED, self.oppositeSpeed)

    def turnRight(self):
        self.setWheelsSpeed(self.oppositeSpeed, SPEED)

    def managePathStatus(self, status):
        if (status == GO_DX):
            self.setWheelsSpeed(-SPEED, SPEED)
        elif (status == GO_SX):
            self.setWheelsSpeed(SPEED, -SPEED)
        elif (status == CROSS):
            self.handleCross()
        elif (status == OBS_FOUNDED):
            self.collisionAvoidance()
        else:
            self.setWheelsSpeed(SPEED, SPEED)

    def stepRotation(self, rotationTime):
        while self.robot.getTime() < rotationTime:
            self.robot.step(int(self.robot.getBasicTimeStep()))

    def handleCross(self):
        newAngle = self.pathManager.popDirection()

        if np.isnan(newAngle):
            newAngle = self.pathManager.getRobotAngleWithCheck()

        self.rotateRobot(newAngle, uTurn=self.isStarted)
        self.pathManager.updatePosition()

    def collisionAvoidance(self):
        self.stopMoving()
        Logger.info('Ostatacolo presente dopo l\'attesa. Avvio procedura di Collision Avoidance')
        if self.isCollisionAvoidance:
            return
        self.stopMoving()
        self.isCollisionAvoidance = True
        self.pathManager.setStartPosition(self.pathManager.currentPosition)
        self.pathManager.updateObstaclesInMap()
        self.pathManager.setStatus(COMPUTING)
        self.rotateRobot(self.pathManager.uTurn(), uTurn=True)
        self.setWheelsSpeed(SPEED, SPEED)
        self.isCollisionAvoidance = False

    # Calcola il tempo necessario a effettuare la rotazione
    # newAngle è l'angolo che deve avere il robot rispetto al Nord
    #  Non è l'angolo di rotazione
    def rotateRobot(self, newAngle, uTurn=False):
        currentAngle = self.pathManager.getRobotAngleWithoutCheck()
        self.pathManager.updateClockwise(newAngle, currentAngle)
        differenceAngle = self.calculateDifferenceAngle(currentAngle, newAngle)
        timeToRotate = self.robot.getTime() + self.pathManager.calculateRotationTime(differenceAngle)

        #Se l'angolo è uguale al precedente e non ho una collision allora vado dritto
        if not self.isCollisionAvoidance and not np.isnan(self.pathManager.getLastDirection()) and self.pathManager.getLastDirection() == newAngle:
            return

        if differenceAngle == 0 or (
                newAngle - 10 < currentAngle < newAngle + 10 and not self.isStarted and differenceAngle != 0):
            Logger.debug(f"Same angles: {currentAngle} <--> {newAngle}")
            return

        self.oppositeSpeed = -SPEED if uTurn else 0

        if self.pathManager.isClockwise():
            print('--> Rotate to right -->')
            self.turnRight()
        else:
            print('<-- Rotate to left <--')
            self.turnLeft()

        if not uTurn or self.isStarted:
            self.pathManager.setLastDirection(newAngle)
        self.stepRotation(timeToRotate)
        self.setWheelsSpeed(SPEED, SPEED)

    def calculateDifferenceAngle(self, start, end):
        diffAngle = self.getDiffAngleFromClockwise(start, end)

        if (end == NORTH and WEST - 10 < start < WEST + 10) or (end == NORTH and EAST - 10 < start < EAST + 10):
            diffAngle = self.getDiffAngleFromClockwise(start, 90)

        if (end == SOUTH and WEST - 10 < start < WEST + 10) or (end == SOUTH and EAST - 10 < start < EAST + 10):
            diffAngle = self.getDiffAngleFromClockwise(start, -90)

        if end == EAST:
            if ((NORTH - 10 < start < NORTH + 10) or 360 - 10 < start < 360):
                diffAngle = 90
            elif (SOUTH - 10 < start < SOUTH + 10):
                diffAngle = 90
            elif EAST - 10 < start < EAST + 10 and self.isStarted:
                diffAngle = 180

        if end == WEST:
            if ((NORTH - 10 < start < NORTH + 10) or 360 - 10 < start < 360):
                diffAngle = 180
            elif (SOUTH - 10 < start < SOUTH + 10):
                diffAngle = 90
            elif WEST - 10 < start < WEST + 10 and self.isStarted:
                diffAngle = 180

        return self.utilController.checkAndApproximateAngle(diffAngle)

    def getDiffAngleFromClockwise(self, start, end):
        if self.pathManager.isClockwise():
            diffAngle = start + end
        else:
            diffAngle = start - end
        return diffAngle

    def goalReached(self):
        self.stopMoving()
