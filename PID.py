from Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_DCMotor, Emakefun_Servo
from simple_pid import PID
import RPi.GPIO as GPIO
from hx711 import HX711
import time
import atexit
import numpy as np

def turnOffMotors():
	mh.getMotor(1).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(2).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(3).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(4).run(Emakefun_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

#set loadcell HX711 GPIO pin 
GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
left_loadcell = HX711(dout_pin = 5, pd_sck_pin = 6)
right_loadcell = HX711(dout_pin = 17, pd_sck_pin = 18)

def load_value(left_button, right_button ):
    if (left_button):
        #return left load value from load cell
        print("left button")
        return ((np.mean(left_loadcell.get_raw_data(2)) + 4000) * 0.005992660189799534) / 1000 #multiply value to calibrated factor, loadcell.factor1() 
    elif (right_button):
        #return right load value from load cell
        print("right button")
        return ((np.mean(right_loadcell.get_raw_data(2)) - 22600) * 0.004655750112110463) / 1000 #multiply value to calibrated factor, loadcell.factor2()
    else:
        return 0.00

# Initialize the motor HAT
mh = Emakefun_MotorHAT(addr=0x60)
left_valve = mh.getMotor(1)
right_valve = mh.getMotor(2)
pump = mh.getMotor(3)

def reset():
    #turn off pump 
    #turn off valve
    left_valve.run(Emakefun_MotorHAT.RELEASE)
    right_valve.run(Emakefun_MotorHAT.RELEASE)
    pump.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(5)
    print("system reset done")

# Initialize the PID controller
desired_load = 2.5  # Desired load value, adjust as needed
pid = PID(30, 0.0, 0.0, setpoint=desired_load)
pid.output_limits = (0, 255) #Adjust based on your pump/valve control

def pid_control(current_load, target_load, left_button, right_button):
	# Calculate the PID output based on the current load
	print(f"current load: {current_load}")
	control_signal = pid(current_load)
	print(f"control siganl: {control_signal}")
	
	# Control logic based on the PID output
	if control_signal > 0: 
		# Need to increase load
		pump_on()
		if left_button:
			inflate_left(control_signal)
			print("left pump")
		else:
			inflate_right(control_signal)
			print("right pump")
			
	elif control_signal < 0:
		# Need to decrease load
		pump_off()
		
		if left_button:
			deflate_left(int(abs(control_signal)))
			print("left release")
		else:
			deflate_right(int(abs(control_signal)))
			print("right release")

	else:
		# Hold current state
		pump_off()
		if left_button:
			hold_left()
			print("left hold air")
		elif right_button:
			hold_right()
			print("right hold air")
            
#--------------------------------------            

def pump_on():
    # Motor pump at speed 100
    pump.setSpeed(255) 
    pump.run(Emakefun_MotorHAT.FORWARD) 

def pump_off():
    pump.run(Emakefun_MotorHAT.RELEASE)

def inflate_left(speed):
    left_valve.setSpeed(speed)
    left_valve.run(Emakefun_MotorHAT.FORWARD) 

    right_valve.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(0.1)

def hold_left():
    left_valve.setSpeed(255) #turn off left valve without releasing air
    left_valve.run(Emakefun_MotorHAT.BACKWARD)

def deflate_left(speed):
    # deflate left for 0.1s
    left_valve.setSpeed(speed)
    left_valve.run(Emakefun_MotorHAT.FORWARD)
    
    right_valve.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(0.1)


def inflate_right(speed):
    #right valve on 
    right_valve.setSpeed(speed)
    right_valve.run(Emakefun_MotorHAT.FORWARD) #turn on left valve motor 
    #left valve off
    left_valve.setSpeed(0) #turn off right valve motor, releasing air
    left_valve.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(0.1)

def hold_right():
    right_valve.setSpeed(255) #turn off left valve without releasing air
    right_valve.run(Emakefun_MotorHAT.BACKWARD)

def deflate_right(speed):
    # deflate right for 0.1s
    right_valve.setSpeed(speed)
    right_valve.run(Emakefun_MotorHAT.FORWARD)
    time.sleep(0.1)  

def reset():
    #turn off pump 
    #turn off valve
    left_valve.run(Emakefun_MotorHAT.RELEASE)
    right_valve.run(Emakefun_MotorHAT.RELEASE)
    pump.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(5)
    print("system reset done")
            
            
            
            
            
            
 #-------------------------------------           

# Main loop
try: 
	while True:
		current_load = load_value(0,1)  # Read the current load from the sensor
		
		# Assuming the target load and button states are provided
		target_load = desired_load  # You can adjust this as needed
		left_button = True  # Replace with actual button state
		right_button = False  # Replace with actual button state
		
		pid_control(current_load, target_load, 0, 1)
		
		# Wait a short period before the next loop iteration
		time.sleep(0.1)
except(KeyboardInterrupt):
	exit()
