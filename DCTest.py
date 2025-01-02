#!/usr/bin/python
from Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_DCMotor, Emakefun_Servo

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Emakefun_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(2).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(3).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(4).run(Emakefun_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
valve = mh.getMotor(2)
pump = mh.getMotor(3)



while (True):	
	################# pump forward test #####################
	
	# set the speed to start, from 0 (off) to 255 (max speed)
	pump.setSpeed(80)
	pump.run(Emakefun_MotorHAT.FORWARD)

	print ("Forward! ")
    
	print ("\tSpeed 20")
	valve.setSpeed(20)
	valve.run(Emakefun_MotorHAT.FORWARD)
	time.sleep(3)
	
	print ("\tSpeed 100")
	valve.setSpeed(100)
	valve.run(Emakefun_MotorHAT.FORWARD)
	time.sleep(3)
	
	print ("\tSpeed 255")
	valve.setSpeed(255)
	valve.run(Emakefun_MotorHAT.BACKWARD)
	time.sleep(6)
	
	print ("Release")
	valve.run(Emakefun_MotorHAT.RELEASE)
	time.sleep(3.0)
	
################# pump backward test #####################
	
	# # set the speed to start, from 0 (off) to 255 (max speed)
	# pump.setSpeed(150)
	# pump.run(Emakefun_MotorHAT.FORWARD)
	# valve.setSpeed(255)
	# valve.run(Emakefun_MotorHAT.FORWARD)

	# time.sleep(3)

	# print ("Backward! ")
    
	# print ("\tSpeed 20")
	# valve.setSpeed(20)
	# valve.run(Emakefun_MotorHAT.BACKWARD)
	# time.sleep(6)
	
	# print ("Release")
	# valve.run(Emakefun_MotorHAT.RELEASE)
	# time.sleep(3.0)

	
	# pump.setSpeed(150)
	# pump.run(Emakefun_MotorHAT.FORWARD)
	# valve.setSpeed(255)
	# valve.run(Emakefun_MotorHAT.FORWARD)

	# time.sleep(3)
	
	# print ("\tSpeed 100")
	# valve.setSpeed(100)
	# valve.run(Emakefun_MotorHAT.BACKWARD)
	# time.sleep(6)
	
	# print ("Release")
	# valve.run(Emakefun_MotorHAT.RELEASE)
	# time.sleep(3.0)
	
	# pump.setSpeed(150)
	# pump.run(Emakefun_MotorHAT.FORWARD)
	# valve.setSpeed(255)
	# valve.run(Emakefun_MotorHAT.FORWARD)

	# time.sleep(3)
	
	# print ("\tSpeed 255")
	# valve.setSpeed(255)
	# valve.run(Emakefun_MotorHAT.BACKWARD)
	# time.sleep(6)
	
	# print ("Release")
	# valve.run(Emakefun_MotorHAT.RELEASE)
	# time.sleep(3.0)
	
	


################### pump test ######################	
	
		# print ("Forward! ")

	# print ("\tSpeed up...")
	# for i in range(80):
		# pump.setSpeed(i)
		# pump.run(Emakefun_MotorHAT.FORWARD)
		# time.sleep(0.05)

	# print ("\tSlow down...")
	# for i in reversed(range(80)):
		# pump.setSpeed(i)
		# pump.run(Emakefun_MotorHAT.FORWARD)
		# time.sleep(0.05)

	# print ("Backward! ")
    
	# print ("\tSpeed up...")
	# for i in range(80):
		# pump.setSpeed(i)
		# pump.run(Emakefun_MotorHAT.BACKWARD)
		# time.sleep(0.05)

	# print ("\tSlow down...")
	# for i in reversed(range(80)):
		# pump.setSpeed(i)
		# pump.run(Emakefun_MotorHAT.BACKWARD)
		# time.sleep(0.05)

	# print ("Release")
	# pump.run(Emakefun_MotorHAT.RELEASE)
	# time.sleep(1.0)
