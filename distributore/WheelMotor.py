
class WheelMotor:
    
    def __init__(self, robot, motorName):
        self.motor = robot.getDevice(motorName)
        self.motor.setPosition(float('inf'))
        self.motor.setVelocity(0.0)
        
    def setMotorSpeed(self, speed):
        self.motor.setVelocity(speed)
        
    
