#All the function of the control system function 
from Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_DCMotor, Emakefun_Servo
import ADS1263
#import Calibrate_loadcell as loadcell
# import RPi.GPIO as GPIO
# from hx711 import HX711
import time
import atexit
import numpy as np

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

# Initialize the motor HAT
mh = Emakefun_MotorHAT(addr=0x60)
left_valve = mh.getMotor(1)
right_valve = mh.getMotor(2)
pump = mh.getMotor(3)

# set motor spedd 
left_valve.setSpeed(255)
right_valve.setSpeed(255)
 
#set loadcell HX711 GPIO pin 
# GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
# left_loadcell = HX711(dout_pin = 5, pd_sck_pin = 6)
# right_loadcell = HX711(dout_pin = 17, pd_sck_pin = 18)

def bang_control(current_load, target_load, pump_switch):
    #bang control method, to switch on or switch off the pump base on current load
    upper_threshold = target_load + 0.5
    lower_threshold = target_load - 0.5
    if (current_load > upper_threshold):
        return False #turn off pump, to reduce load
    elif (current_load <= upper_threshold, current_load >= lower_threshold):
        if (pump_switch == False):
            return False
        elif (pump_switch == True):
            return True
    else:
        return True


def pump_on():
    #turn on pump
    pump.setSpeed(255) #set pump motor speed  
    pump.run(Emakefun_MotorHAT.FORWARD) #turn on pump motor 

def pump_off():
    #turn off pump
    pump.run(Emakefun_MotorHAT.RELEASE) #turn off pump motor 

def valve_left_on():
    #left valve on 
    left_valve.setSpeed(255)
    left_valve.run(Emakefun_MotorHAT.FORWARD) #turn on left valve motor 
    #right valve off
    right_valve.setSpeed(0) #turn off right valve motor, without releasing air

def valve_left_off():
    left_valve.setSpeed(0) #turn off left valve without releasing air

def valve_left_air_release():
    #left valve turn off and release air
    left_valve.run(Emakefun_MotorHAT.RELEASE) #turn off and release air  

def valve_right_on():
    #right valve on 
    right_valve.setSpeed(255)
    right_valve.run(Emakefun_MotorHAT.FORWARD) #turn on left valve motor 
    #left valve off
    left_valve.setSpeed(0) #turn off right valve motor,without releasing air

def valve_right_off():
    right_valve.setSpeed(0) #turn off right valve without releasing air

def valve_right_air_release():
    #right valve turn off and release air
    right_valve.run(Emakefun_MotorHAT.RELEASE) #turn off and release air  


def pressure_value():
    # to initialize pressure sensor
    ADC = ADS1263.ADS1263()
    # to read pressure value from pressure sensor
    if (ADC.ADS1263_init_ADC1('ADS1263_400SPS') == -1):
        exit()
    ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel
    if(TEST_ADC1):       # ADC1 Test
        channelList = [0]  # The channel must be less than 10
        while(1):
            ADC_Value = ADC.ADS1263_GetAll(channelList)    # get ADC1 value
            for i in channelList:
                if(ADC_Value[i]>>31 ==1):
                    # print("ADC1 IN%d = -%lf" %(i, (REF*2 - ADC_Value[i] * REF / 0x80000000)))  
                    voltage = (REF*2 - ADC_Value[i] * REF / 0x80000000)
                else:
                    # print("ADC1 IN%d = %lf" %(i, (ADC_Value[i] * REF / 0x7fffffff)))   # 32bit
                    voltage = (REF*2 - ADC_Value[i] * REF / 0x80000000)
            # for i in channelList:
            #     print("\33[2A")
        
    #return pressure value from the pressure sensor
    value = 42.676 * voltage - 0.7838
    return value
    

def left_load_value():
    #return left load value from load cell
    #return np.mean(left_loadcell.get_raw_data()) * loadcell.factor1() #multiply value to calibrated factor, loadcell.factor1() 
    pass

def right_load_value():
    #return right load value from load cell
    #return np.mean(right_loadcell.get_raw_data()) * loadcell.factor2() #multiply value to calibrated factor, loadcell.factor2() 
    pass

def reset():
    #turn off pump 
    #turn off valve
    left_valve.run(Emakefun_MotorHAT.RELEASE)
    right_valve.run(Emakefun_MotorHAT.RELEASE)
    pump.run(Emakefun_MotorHAT.RELEASE)
    print("system reseted")
    #implement code to release air from airbag
