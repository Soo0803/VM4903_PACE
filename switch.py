#!/usr/bin/python
from Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_DCMotor, Emakefun_Servo
import time
import atexit

# Initialize the motor HAT
mh = Emakefun_MotorHAT(addr=0x60)

# Function to turn off all motors
def turnOffMotors():
    mh.getMotor(1).run(Emakefun_MotorHAT.RELEASE)
    mh.getMotor(2).run(Emakefun_MotorHAT.RELEASE)
    mh.getMotor(3).run(Emakefun_MotorHAT.RELEASE)
    mh.getMotor(4).run(Emakefun_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

# Select the motor port for the myMotor (1-4)
valve1 = mh.getMotor(1)
valve2 = mh.getMotor(2)
pump = mh.getMotor(3)


# Main loop
while True:
    #Activate pump
    pump.setSpeed(255) #Max power
    pump.run(Emakefun_MotorHAT.FORWARD)
    
    # Activate valve1
    valve1.setSpeed(255)  # Maximum power
    valve1.run(Emakefun_MotorHAT.FORWARD)
    time.sleep(0.25)  # myMotor is active for 1 second

    # Activate valve2
    valve2.setSpeed(255)  # Maximum power
    valve2.run(Emakefun_MotorHAT.FORWARD)
    time.sleep(0.25)  # myMotor is active for 1 second

    # Deactivate valve1
    valve1.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(0.25)  # myMotor is off for 1 second

    # Deactivate valve2
    valve2.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(0.25)  # myMotor is off for 1 second    
