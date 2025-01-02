from hx711 import HX711
import RPi.GPIO as GPIO
  
GPIO.setmode(GPIO.BCM)                 # set GPIO pin mode to BCM numbering
loadcell_1 = HX711(dout_pin = 5, pd_sck_pin = 6)
loadcell_2 = HX711(dout_pin = 17, pd_sck_pin = 18)

loadcell_1.zero()
loadcell_2.zero()

while True:
    weight_1 = loadcell_1.get_raw_data()
    weight_2 = loadcell_2.get_raw_data()

