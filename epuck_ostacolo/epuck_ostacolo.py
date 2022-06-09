from controller import Robot

# Get reference to the robot.
robot = Robot()

# Get simulation step length.
timeStep = int(robot.getBasicTimeStep())

# Constants of the e-puck motors and distance sensors.
maxMotorVelocity = 2

# Get left and right wheel motors.
leftMotor = robot.getDevice("left wheel motor")
rightMotor = robot.getDevice("right wheel motor")

# Get frontal distance sensors.
frontSensor = robot.getDevice("distance_front") 
frontSensor.enable(timeStep)

# Get back distance sensors.
rightSensor = robot.getDevice("distance_right") 
rightSensor.enable(timeStep)

# Disable motor PID control mode.
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

# Set ideal motor velocity.
initialVelocity = 0.7 * maxMotorVelocity

# Set the initial velocity of the left and right wheel motors.
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

while robot.step(timeStep) != -1:
    frontValue = frontSensor.getValue()
    rightValue = rightSensor.getValue()

    if frontValue < 500:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)

    if rightValue < 800:
        leftMotor.setVelocity(initialVelocity)
        rightMotor.setVelocity(initialVelocity)
