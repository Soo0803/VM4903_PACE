#All the function of the control system function 
from Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_DCMotor, Emakefun_Servo
import ADS1263
#import Calibrate_loadcell as loadcell
import RPi.GPIO as GPIO
from hx711 import HX711
import time
import atexit
import numpy as np
from simple_pid import PID
import reloadable
import matplotlib.pyplot as plt


# pressure sensor initialize (ADS1263 module)
REF = 5.00          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V
# ADC1 test part
TEST_ADC1       = True
# ADC2 test part
TEST_ADC2       = False
# ADC1 rate test part, For faster speeds use the C program
TEST_ADC1_RATE   = False
# RTD test part 
TEST_RTD        = False     


ADC = ADS1263.ADS1263()

# The faster the rate, the worse the stability
#and the need to choose a suitable digital filter(REG_MODE1)
if (ADC.ADS1263_init_ADC1('ADS1263_400SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel
# print("exit line 32")

old_target_load = [0]
achieved = [0] # target achieve is 1 when the the pump overshoor the target load first time, when 2 stop the pid system
print("system success")

# Initialize the motor HAT
mh = Emakefun_MotorHAT(addr=0x60)
left_valve = mh.getMotor(1)
right_valve = mh.getMotor(2)
pump = mh.getMotor(3)

def turnOffMotors():
	mh.getMotor(1).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(2).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(3).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(4).run(Emakefun_MotorHAT.RELEASE)

atexit.register(turnOffMotors)


# # set motor spedd 
# left_valve.setSpeed(255)
# right_valve.setSpeed(255)
 
#set loadcell HX711 GPIO pin 
GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
left_loadcell = HX711(dout_pin = 5, pd_sck_pin = 6)
right_loadcell = HX711(dout_pin = 12, pd_sck_pin = 13)

print("GPIO set")

def pump_on(speed):
    # turn on pump
    pump.setSpeed(int(speed))  # set pump motor speed
    pump.run(Emakefun_MotorHAT.FORWARD)  # turn on pump motor

def pump_off():
    # turn off pump
    pump.setSpeed(0) 
    pump.run(Emakefun_MotorHAT.RELEASE)  # turn off pump motor

def valve_left_on():
    print("enter valve left on")
    # left valve on 
    left_valve.setSpeed(255)
    left_valve.run(Emakefun_MotorHAT.FORWARD)  # turn on left valve motor
    # right valve off
    right_valve.setSpeed(0)  # turn off right valve motor, releasing air
    right_valve.run(Emakefun_MotorHAT.RELEASE)

def valve_left_off():
    left_valve.setSpeed(255)  # turn off left valve without releasing air
    left_valve.run(Emakefun_MotorHAT.BACKWARD)

def valve_left_air_release(release_speed):
    # left valve turn off and release air
    left_valve.setSpeed(release_speed)
    left_valve.run(Emakefun_MotorHAT.RELEASE)  # turn off and release air for 0.05 second
    time.sleep(0.01)
    left_valve.setSpeed(255)
    left_valve.run(Emakefun_MotorHAT.FORWARD)

def valve_right_on():
    # right valve on 
    right_valve.setSpeed(255)
    right_valve.run(Emakefun_MotorHAT.FORWARD)  # turn on left valve motor
    # left valve off
    left_valve.setSpeed(0)  # turn off right valve motor, releasing air
    left_valve.run(Emakefun_MotorHAT.RELEASE)

def valve_right_off():
    right_valve.setSpeed(255)  # turn off left valve without releasing air
    right_valve.run(Emakefun_MotorHAT.BACKWARD)

def valve_right_air_release(release_speed):
    # right valve turn off and release air
    right_valve.setSpeed(release_speed)
    right_valve.run(Emakefun_MotorHAT.RELEASE)  # turn off and release air for 0.05 second
    time.sleep(0.01)
    right_valve.setSpeed(255)
    right_valve.run(Emakefun_MotorHAT.FORWARD)

class PIDController:
    def __init__(self):
        self.is_holding = False
        self.old_target = 0.00

    def pid_control(self, current_load, target_load, left_button, right_button, pump_status):
        if pump_status is False:
            print("pump off")
            return
            
        if self.old_target != target_load:
            self.is_holding = False
            self.old_target = target_load
            
        if self.is_holding:
            print("----------------HOLD (Persistent)")
            #pump_on(57)
            pump_off()
            if left_button:
                valve_left_off()
            elif right_button:
                valve_right_off()
            print(f"target load: {target_load}")
            print(f"current load: {current_load}")
            load_difference = abs(target_load - current_load)
            print(f"load difference: {target_load - current_load}")
            return

        # PID constants
        Kp = 40.0
        Ki = 30.0
        Kd = 0.0

        pid = PID(Kp, Ki, Kd, setpoint=target_load)
        pid.output_limits = (-255, 255)  # Adjust according to your pump control limits

        control_signal = pid(current_load)
        print(f"target load: {target_load}")
        print(f"current load: {current_load}")
        print(f"control signal: {control_signal}")

        load_difference = abs(target_load - current_load)
        print(f"load difference: {target_load - current_load}")

        if load_difference < 0.1:
            print("----------------HOLD")
            # hold air
            #pump_on(57)
            pump_off()
            self.is_holding = True
            if left_button:
                valve_left_off()
            elif right_button:
                valve_right_off()

        elif control_signal > 0:
            print("--------------INFLATE")
            # inflate airbag
            if left_button:
                valve_left_on()
            elif right_button:
                valve_right_on()
            if load_difference < 1:
                control_signal = control_signal * 3.0
            pump_on(control_signal)

        elif control_signal < 0:
            print("--------------DEFLATE")
            # deflate air
            if left_button:
                valve_left_air_release(1)
            elif right_button:
                valve_right_air_release(abs(control_signal))
            pump_off()

# def pid_control(current_load, target_load, left_button, right_button, pump_status):   
    # print("pid enter") 
    # # print ("first line old target load = ", old_target_load[0])
    # #print ("target achieved = ", achieved[0])


    # print("pid pass") 
    # # if target_load != old_target_load[0]:
        # # print("target load changed")
        # # #achieved = [0]
        # # old_target_load[0] = target_load
        # # print ("old target load = ", old_target_load[0])
        
    # if pump_status is False:
        # pump_off()
        # if (achieved[0] == 2):
            # print("target achieved")
        # return
    # # elif (abs(current_load - target_load) <= 0.09):
        # # pump_off()
        # # print(f" pump off current load: {current_load}")
        # # print("target load reached, holding")
        # # return
        
        
    # # PID constants
    # Kp = 40.0
    # Ki = 10.0
    # Kd = 0

    # pid = PID(Kp, Ki, Kd, setpoint= target_load)
    # pid.output_limits = (-255, 255)  # Adjust according to your pump control limits

    # control_signal = pid(current_load)
    # print(f"current load: {current_load}")
    # #print("target achieve = ",achieved[0])
    
    # if control_signal > 0: 
        # # inflate airbag
        # if left_button:
            # valve_left_on()
        # elif right_button:
            # valve_right_on()
        # control_signal = control_signal * 2
        # if(control_signal < 40):
            # if (target_load >= 6.5):
                # control_signal = 60
            # else:
                # control_signal = 50
        # elif (control_signal >= 255):
            # control_signal = 255
        # pump_on(control_signal)
        # print(f"                                control signal: {control_signal}")
    # elif control_signal < 0:
        # # deflate air
        # if left_button:
            # valve_left_air_release(1)
        # elif right_button:
            # valve_right_air_release(1)
        # pump_off()
    # else:
        # # hold air
        # if left_button:
            # valve_left_off()
        # elif right_button:
            # valve_right_off()
            
    # if abs(target_load - current_load) <= 0.1:
        # print("target and current diff is ideal")
        # #achieved[0] += 1
        

    
    
    # time = np.linspace(0, 10, 100)  # 10 seconds, 100 points
    # measured_value = 0
    # output = []
    # for t in time:
        # output.append(current_load)

# # Plot the results

    # plt.plot(time, output, label='Output')
    # plt.axhline(y=5, color='r', linestyle='--', label='Setpoint')
    # plt.xlabel('Time')
    # plt.ylabel('Output')
    # plt.legend()
    # plt.show()
            




# def bang_control(current_load, target_load,left_button, right_button):
    # #bang control method, to switch on or switch off the pump base on current load
    # print("enter bang control")
    # upper_threshold = target_load + target_load * 0.1
    # lower_threshold = target_load - target_load * 0.1
    # if ((target_load - current_load) <= 2):
        # pump.setSpeed(30)
        # print("pump speed adjust to 30")
        # pump.run(Emakefun_MotorHAT.FORWARD) #change pump motor speed to 50
    # elif ((target_load - current_load) <= 1):
        # pump.setSpeed(10)
        # print("pump speed adjust to 30")
        # pump.run(Emakefun_MotorHAT.FORWARD) #change pump motor speed to 10
    # elif ((target_load - current_load) <= 0.5):
        # pump. setSpeed(5)
        # print("pump speed adjust to 5")
        # pump.run(Emakefun_MotorHAT.FORWARD) #change pump motor speed to 5
    # elif ((target_load - current_load) <= 0.15):
        # pump.setSpeed(2)
        # print("pump speed adjust to 2")
        # pump.run(Emakefun_MotorHAT.FORWARD)
    # elif ((target_load - current_load) <= -0.15):
        # if (left_button):
            # valve_left_air_release(5)
            # print("valve left air release speed adjust to 5")
        # elif(right_button):
            # valve_right_air_release(5)
            # print("valve right air release speed adjust to 5")
    # elif ((target_load - current_load <= -0.5)):
        # if (left_button):
            # valve_left_air_release(10)
            # print("valve left air release speed adjust to 10")
        # elif(right_button):
            # valve_right_air_release(10)
            # print("valve right air release speed adjust to 10")
    # elif ((target_load - current_load <= -1)):
        # if (left_button):
            # valve_left_air_release(50)
            # print("valve left air release speed adjust to 50")
        # elif(right_button):
            # valve_right_air_release(50)
            # print("valve right air release speed adjust to 50")
    # elif (abs(target_load - current_load) <= 0.05):
            # pump.run(Emakefun_MotorHAT.RELEASE)


      



def pressure_value():
    if(TEST_ADC1):       # ADC1 Test
        channelList = [0]  # The channel must be less than 10
        ADC_Value = ADC.ADS1263_GetAll(channelList)    # get ADC1 value
        for i in channelList:
            if(ADC_Value[i]>>31 ==1):
                # print("current_pressure : %d = -%lf" %(i, (REF*2 - ADC_Value[i] * REF / 0x80000000)))  
                value_1 = (REF*2 - ADC_Value[i] * REF / 0x80000000)
            else:
                # print("current_pressure 2 : %d = %lf" %(i, (ADC_Value[i] * REF / 0x7fffffff)))   # 32bit
                voltage = (ADC_Value[i] * REF / 0x7fffffff)
        for i in channelList:
            print("\33[2A")
    #return pressure value from the pressure sensor
    value = 42.676 * voltage - 0.7838
    return value
    

def load_value(left_button, right_button ):
    if (left_button):   
        #return left load value from load cell
        print("left button")
        return ((np.mean(left_loadcell.get_raw_data(10)) + 4000) * 0.005992660189799534) / 1000 #multiply value to calibrated factor, loadcell.factor1() 
    elif (right_button):
        #return right load value from load cell
        print("right button")
        return ((np.mean(right_loadcell.get_raw_data(10)) - 22600) * 0.004655750112110463) / 1000 #multiply value to calibrated factor, loadcell.factor2()
    else:
        return 0.00


def reset():
    #turn off pump 
    #turn off valve
    left_valve.setSpeed(255)
    right_valve.setSpeed(255)
    left_valve.run(Emakefun_MotorHAT.RELEASE)
    right_valve.run(Emakefun_MotorHAT.RELEASE)
    pump.run(Emakefun_MotorHAT.RELEASE)
    print("system reseted")
    #implement code to release air from airbag
    
# try:
    # while True:
        # curr_load = load_value(1,0)
        # target_load = 4.0
        # pid_control(curr_load, target_load, 1, 0,1)
# except(KeyboardInterrupt):
    # turnOffMotors()
    # exit()
    
    
# def bang_control(current_load, target_load,left_button, right_button):
    # #bang control method, to switch on or switch off the pump base on current load
    # upper_threshold = target_load + target_load * 0.1
    # lower_threshold = target_load - target_load * 0.1
    # if (current_load > upper_threshold):
         # #turn off pump, to reduce load
        # if (left_button):
            # valve_left_air_release(30)
            # print("left release")
        # else:
            # valve_right_air_release(30)
            # print("right release")
    # elif (current_load <= upper_threshold, current_load >= lower_threshold):
        # if (left_button ):
            # valve_left_off()
            # print("left off")
        # elif (right_button):
            # valve_right_off()
            # print("right off")
    # elif (current_load < target_load):
        # if (left_button):
            # valve_left_on()
            # print("left on")
        # elif(right_button):
            # valve_right_on()
            # print("right on")
    # elif (current_load >= target_load):
        # if (left_button):
            # left_valve.setSpeed(50)
            # print("left speed 50")
        # elif(right_button):
            # right_valve.setSpeed(50)
            # print("right speed 50")
