from Emakefun_MotorHAT import Emakefun_MotorHAT
import GUI 
import ControlSystemFunction as system
import time
from ControlSystemFunction import PIDController

foot_comfort_button_pressed_time = None


#target_load and current_load is already define in GUI.py
# current_load = 0.0
# target_load = 4.0
current_pressure = 0.0
pump_switch = False
# target_achieved = 0; # target achieve is 1 when the the pump overshoor the target load first time, when target_achieved = 2 stop the pid system
# old_target_load = 0;

#set a counter to count how many time current pressure exceed 90kPa, to elimate noise 
pressure_limit_counter = 0

# boolean to show if the corresponding button is turn on or turn off
reset_triggered = False
is_left_foot_color = False 
is_right_foot_color = False
is_left_foot_active = False
is_right_foot_active = False
is_playing = False
is_star_active = False

# Initialize the motor HAT
mh = Emakefun_MotorHAT(addr=0x60)
left_valve = mh.getMotor(1)
right_valve = mh.getMotor(2)
pump = mh.getMotor(3)


#initiate PID object from system PID class
pid = PIDController()
print("pid object created")

# Correct Byte Commands as per Arduino Master Code
left_foot_command = b'\x01'  # Raw byte command for Left Foot (equivalent to 0x01)
right_foot_command = b'\x02'  # Raw byte command for Right Foot (equivalent to 0x02)
play_pause_command = b'\x03'  # Raw byte command for Play/Pause (equivalent to 0x03)
decrease_load_command = b'\x04'  # Raw byte command for Decrease Load (equivalent to 0x04)
increase_load_command = b'\x05'  # Raw byte command for Increase Load (equivalent to 0x05)
power_command = b'\x06'  # Raw byte command for Power (equivalent to 0x06)
reset_command = b'\x07'  # Raw byte command for Reset (equivalent to 0x07)
no_reset_command = b'\x09'

def get_status_byte():
    # Combine the left and right foot states into a single status byte
    # Adjust the logic to match how your Arduino interprets the status_byte
    return (0x01 if is_left_foot_active else 0x00) | (0x02 if is_right_foot_active else 0x00)

try:
    while True:
        try:
            event, values = GUI.window.read(timeout=100)




            if event == GUI.sg.WIN_CLOSED:
                break



        except Exception as e:
            GUI.sg.popup_error(f"An error occurred: {e}")
            break  # Optionally remove this line if you don't want the window to close after an error


            # Handle foot and play/pause buttons as before
        # ...

        #get pressure reading
        pressure_value = system.pressure_value()
        print("pressure = ", pressure_value)
        #if pressure is above 90kPa turn off the system and reset
        if (pressure_value > 80):
            pressure_limit_counter += 1
            if (pressure_limit_counter > 2):
                print("device exceed pressure limit")
                pressure_limit_counter = 0
                system.reset()
                time.sleep(5)



        # Update the target load based on Plus or Minus buttons
            # Toggle Left Foot      
        if event == '-LEFT-FOOT-':
            is_left_foot_color = True  # Turn the left foot on
            is_right_foot_color = False  # Turn the right foot off

            is_left_foot_active = not is_left_foot_active

            # Update Left Foot Image
            current_left_image = GUI.left_foot_color_image if is_left_foot_color else GUI.left_foot_grey_image
            GUI.window['-LEFT-FOOT-'].update(image_filename = GUI.resize_image(current_left_image, 350, 700))

            # Update Right Foot Image to Grey
            current_right_image = GUI.right_foot_grey_image
            GUI.window['-RIGHT-FOOT-'].update(image_filename = GUI.resize_image(current_right_image, 350, 700))
            
            if is_left_foot_color :
                system.valve_left_on()
                print("left")

            # Toggle Right Foot
        elif event == '-RIGHT-FOOT-':
            is_left_foot_color = False  # Turn the left foot off
            is_right_foot_color = True  # Turn the right foot on

            is_right_foot_active = not is_right_foot_active

            # Update Right Foot Image
            current_right_image = GUI.right_foot_color_image if is_right_foot_color else GUI.right_foot_grey_image
            GUI.window['-RIGHT-FOOT-'].update(image_filename = GUI.resize_image(current_right_image, 350, 700))

            # Update Left Foot Image to Grey
            current_left_image = GUI.left_foot_grey_image
            GUI.window['-LEFT-FOOT-'].update(image_filename = GUI.resize_image(current_left_image, 350, 700))

            if is_right_foot_color :
                system.valve_right_on()
                print("right")

            # Toggle Play/Pause
        elif event == '-PLAY-PAUSE-':
            is_playing = not is_playing  # Toggle state
            new_image = GUI.pause_button_orange if is_playing else GUI.play_button_grey
            GUI.window['-PLAY-PAUSE-'].update(image_filename = GUI.resize_image(new_image, 100, 100))

        elif event == '-PLUS-' and GUI.target_load < 20:
            GUI.target_load += 0.5
            GUI.window['-TARGET-LOAD-'].update(f'{GUI.target_load:.2f} kg')

        elif event == '-MINUS-' and GUI.target_load > 0:
            GUI.target_load -= 0.5
            GUI.window['-TARGET-LOAD-'].update(f'{GUI.target_load:.2f} kg')

        # Toggle the star button's state and update its image
        elif event == '-STAR-':
            is_star_active = not is_star_active
            new_image = GUI.star_button_orange if is_star_active else GUI.star_button_grey
            GUI.window['-STAR-'].update(image_filename = GUI.resize_image(new_image, 100, 100))

        if is_star_active:
            system.reset()
            
        GUI.current_load = system.load_value(is_left_foot_color, is_right_foot_color)
        print("cureen")
        GUI.window['-CURRENT-LOAD-'].update(f'{GUI.current_load:.2f} kg')
        
        
        pid.pid_control(GUI.current_load, GUI.target_load, is_left_foot_color, is_right_foot_color, is_playing)
        
        print("loop end")
        
except(KeyboardInterrupt):
    system.turnOffMotors()
    GUI.window.close()
    exit()
finally:
    system.turnOffMotors()
    GUI.window.close()
    exit()



        
#    if is_star_active and system.bang_control():
#        if is_left_foot_color:
#            system.valve_left_off()
#        elif is_right_foot_color:
#            system.valve_right_off()

    # Implementing long press logic for reset (placeholder)
    # Check for foot comfort button press
    # if event == '-FOOT-COMFORT-BUTTON-':  # Replace with the actual key for your button
    #     if foot_comfort_button_pressed_time is None:
    #         # Record the time the button was first pressed
    #         foot_comfort_button_pressed_time = GUI.time.time()
    #         print(foot_comfort_button_pressed_time)

    # # Check if button was released or long press condition was met
    # if foot_comfort_button_pressed_time is not None:
    #     # Calculate how long the button has been held down
    #     held_down_duration = GUI.time.time() - foot_comfort_button_pressed_time

    #     if held_down_duration >= GUI.LONG_PRESS_DURATION and not reset_triggered:
    #         # Long press detected, mark reset as triggered
    #         reset_triggered = True
    #         print("Reset triggered due to long press")

    #     elif event is None or event != '-FOOT-COMFORT-BUTTON-':
    #         # Button was released before long press duration was met
    #         foot_comfort_button_pressed_time = None


