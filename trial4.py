import PySimpleGUI as sg
import serial
from PIL import Image
import os
import time
import struct
import tkinter as tk

foot_comfort_button_pressed_time = None
LONG_PRESS_DURATION = 2  # Duration for long press in seconds, adjust as needed
reset_triggered = False

sg.theme('Dark')
background_color = sg.theme_background_color()


# try:
#     ser = serial.Serial('COM9', 9600)
#     # Replace 'COM9' with '/dev/ttyUSB0' or the correct port
# #    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
#     # Configure the serial connections (the parameters differ on the device you are connecting to)
#     ser.flush()
# except serial.SerialException:
#     print("Could not open serial port.")

# Correct Byte Commands as per Arduino Master Code
left_foot_command = b'\x01'  # Raw byte command for Left Foot (equivalent to 0x01)
right_foot_command = b'\x02'  # Raw byte command for Right Foot (equivalent to 0x02)
play_pause_command = b'\x03'  # Raw byte command for Play/Pause (equivalent to 0x03)
decrease_load_command = b'\x04'  # Raw byte command for Decrease Load (equivalent to 0x04)
increase_load_command = b'\x05'  # Raw byte command for Increase Load (equivalent to 0x05)
power_command = b'\x06'  # Raw byte command for Power (equivalent to 0x06)
reset_command = b'\x07'  # Raw byte command for Reset (equivalent to 0x07)
no_reset_command = b'\x09'


window_x_position = 100
window_y_position = 100

left_foot_grey_image = 'Lefto.png'
left_foot_color_image = 'Left.png'
right_foot_grey_image = 'Righto.png'
right_foot_color_image = 'Right.png'

is_left_foot_color = False
is_right_foot_color = False
is_left_foot_active = False
is_right_foot_active = False


def get_status_byte():
    # Combine the left and right foot states into a single status byte
    # Adjust the logic to match how your Arduino interprets the status_byte
    return (0x01 if is_left_foot_active else 0x00) | (0x02 if is_right_foot_active else 0x00)

play_button_grey = "play.png"
pause_button_orange = "pause.png"
plus_button_grey = "plus.png"
minus_button_grey = "minus.png"
star_button_grey = "staroff.png"
star_button_orange = "staron.png"

is_playing = False
is_star_active = False
# Initial State Variables
is_left_foot_active = False
is_right_foot_active = False
is_playing = False
target_load = 4.0
current_load = 0.0

# Variables for logo position adjustment
logo_x_offset = 100  # Adjust this to move the logo left or right
logo_y_offset = 50   # Adjust this to move the logo up or down


# Path to your company logo
company_logo_path = 'footlogo.png'

# Ensure the logo is resized and has a consistent background
def prepare_logo(image_path, width, height):
    try:
        if not os.path.exists(image_path):
            raise ValueError(f"Image not found: {image_path}")

        with Image.open(image_path) as image:
            # Resize the image while maintaining aspect ratio
            image.thumbnail((width, height), Image.Resampling.LANCZOS)

            # Convert to 'RGB' if the window background is not transparent
            final_image = Image.new("RGB", image.size, background_color)
            final_image.paste(image, mask=image.split()[3])  # 3 is the alpha channel

            # Save the resized image to a temporary file and return its path
            logo_image_path = f"temp_logo_{os.path.basename(image_path)}"
            final_image.save(logo_image_path, format="PNG")
            return logo_image_path
    except Exception as e:
        sg.popup_error(f"Failed to load or resize logo: {e}")
        return None

# Define the resize_image function here
def resize_image(image_path, desired_width, desired_height):
    try:
        if not os.path.exists(image_path):
            raise ValueError(f"Image not found: {image_path}")

        with Image.open(image_path) as image:
            # Create a new image with uniform background color
            new_image = Image.new("RGBA", image.size)
            new_image.paste(image, (0, 0), image)

            # Resize the image while maintaining transparency
            original_width, original_height = new_image.size
            scale_factor = min(desired_width / original_width, desired_height / original_height)
            new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
            resized_image = new_image.resize(new_size, Image.Resampling.LANCZOS)

            # Convert to 'RGB' if the window background is not transparent
            if background_color != 'transparent':
                final_image = Image.new("RGB", resized_image.size, background_color)
                final_image.paste(resized_image, mask=resized_image.split()[3])  # 3 is the alpha channel
            else:
                final_image = resized_image

            # Save the resized image to a temporary file and return its path
            resized_image_path = f"temp_{os.path.basename(image_path)}"
            final_image.save(resized_image_path, format="PNG")
            return resized_image_path
    except Exception as e:
        sg.popup_error(f"Failed to load or resize image: {e}")
        return None

resized_logo_path = prepare_logo(company_logo_path, 1, 1)  # Adjust the size as needed
    
#resize company_logo 
resize_company_logo_path = 'resize_footlogo.png' 
new_size = (53,35)
try:
    # Open the image file
    with Image.open(company_logo_path) as img:
        # Resize the image
        resized_img = img.resize(new_size)
        # Save the resized image
        resized_img.save(resize_company_logo_path)
    print(f"Image resized and saved to {company_logo_path}")
except Exception as e:
    print(f"Error: {e}")

# Define the create_image_button function here
def create_image_button(image_path, key, size=(100, 100)):
    resized_image_path = resize_image(image_path, size[0], size[1])
    if not resized_image_path:
        return sg.Button('', key=key, visible=False)
    return sg.Button('',
                     image_filename=resized_image_path,
                     key=key,   
                     border_width=0,
                     button_color=(sg.theme_background_color(), sg.theme_background_color()),
                     pad=(5, 5), size=(size[0], size[1]))

# Define the layout here
layout = [
    [sg.Column([
        [sg.Text('', size=(1,1))],
        [create_image_button(left_foot_grey_image, '-LEFT-FOOT-', size=(300, 550))],
    ]),
    sg.Column([
        
        [sg.Text('', size=(1,4))],
        [sg.Text('', size=(1,1)), sg.Text('🎯', font=('Helvetica', 22)), sg.Text(f'{target_load:.1f} kg', key='-TARGET-LOAD-', font=('Helvetica', 18)),
         sg.Text('⚡', font=('Helvetica', 18)),  # Buffer space
         sg.Text(f'{current_load:.1f} kg', key='-CURRENT-LOAD-', font=('Helvetica', 18))],  
        [sg.Text('', size = (11,1)), create_image_button(plus_button_grey, '-PLUS-', size=(100, 100))],
        [create_image_button(play_button_grey, '-PLAY-PAUSE-', size=(100, 100)), sg.Text('', size=(10,1)), create_image_button(star_button_grey, '-STAR-', size=(100, 100))],
        [sg.Text('', size=(11,1)), create_image_button(minus_button_grey, '-MINUS-', size=(100, 100))]
    ]),
    sg.Column([
        [sg.Button(image_filename = resize_company_logo_path, key='-FOOT-COMFORT-BUTTON-', border_width=0, button_color=(background_color, background_color)),
         sg.Text("Foot Comfort Technology", font=("Helvetica", 14))],
        [create_image_button(right_foot_grey_image, '-RIGHT-FOOT-', size=(300, 550))]
    ])]
]

window = sg.Window('Foot Comfort Control', layout, finalize=True, size=(1280, 800), background_color=background_color, default_element_size=(30, 1))

# create window and set the window's location to center it
#...

# Event loop and logic for updating buttons
# ...

# Event loop
while True:
    try:
        event, values = window.read(timeout=100)




        if event == sg.WIN_CLOSED:
            break



    except Exception as e:
        sg.popup_error(f"An error occurred: {e}")
        break  # Optionally remove this line if you don't want the window to close after an error


        # Handle foot and play/pause buttons as before
    # ...

    # Update the target load based on Plus or Minus buttons
        # Toggle Left Foot
    if event == '-LEFT-FOOT-':
        is_left_foot_color = True  # Turn the left foot on
        is_right_foot_color = False  # Turn the right foot off

        is_left_foot_active = not is_left_foot_active

        # Update Left Foot Image
        current_left_image = left_foot_color_image if is_left_foot_color else left_foot_grey_image
        window['-LEFT-FOOT-'].update(image_filename=resize_image(current_left_image, 300, 600))

        # Update Right Foot Image to Grey
        current_right_image = right_foot_grey_image
        window['-RIGHT-FOOT-'].update(image_filename=resize_image(current_right_image, 300, 600))

        # ser.write(get_status_byte())

        # Toggle Right Foot
    elif event == '-RIGHT-FOOT-':
        is_left_foot_color = False  # Turn the left foot off
        is_right_foot_color = True  # Turn the right foot on

        is_right_foot_active = not is_right_foot_active

        # Update Right Foot Image
        current_right_image = right_foot_color_image if is_right_foot_color else right_foot_grey_image
        window['-RIGHT-FOOT-'].update(image_filename=resize_image(current_right_image, 300, 600))

        # Update Left Foot Image to Grey
        current_left_image = left_foot_grey_image
        window['-LEFT-FOOT-'].update(image_filename=resize_image(current_left_image, 300, 600))

        # ser.write(get_status_byte())

        # Toggle Play/Pause
    elif event == '-PLAY-PAUSE-':
        is_playing = not is_playing  # Toggle state
        new_image = pause_button_orange if is_playing else play_button_grey
        window['-PLAY-PAUSE-'].update(image_filename=resize_image(new_image, 100, 100))
        # ser.write(play_pause_command)  # Send byte command

    elif event == '-PLUS-' and target_load < 20:
        target_load += 0.5
        window['-TARGET-LOAD-'].update(f'{target_load:.2f} kg')
        # ser.write(increase_load_command)  # Send byte command

    elif event == '-MINUS-' and target_load > 0:
        target_load -= 0.5
        window['-TARGET-LOAD-'].update(f'{target_load:.2f} kg')
      #  ser.write(decrease_load_command)  # Send byte command

    # Toggle the star button's state and update its image
    elif event == '-STAR-':
        is_star_active = not is_star_active
        new_image = star_button_orange if is_star_active else star_button_grey
        window['-STAR-'].update(image_filename=resize_image(new_image, 100, 100))
     #   ser.write(power_command)  # Send byte command

    # Implementing long press logic for reset (placeholder)
    # Check for foot comfort button press
    if event == '-FOOT-COMFORT-BUTTON-':  # Replace with the actual key for your button
        if foot_comfort_button_pressed_time is None:
            # Record the time the button was first pressed
            foot_comfort_button_pressed_time = time.time()

    # Check if button was released or long press condition was met
    if foot_comfort_button_pressed_time is not None:
        # Calculate how long the button has been held down
        held_down_duration = time.time() - foot_comfort_button_pressed_time

        if held_down_duration >= LONG_PRESS_DURATION and not reset_triggered:
            # Long press detected, mark reset as triggered
            reset_triggered = True
            print("Reset triggered due to long press")

        elif event is None or event != '-FOOT-COMFORT-BUTTON-':
            # Button was released before long press duration was met
            foot_comfort_button_pressed_time = None

    # Send the appropriate reset command
    # if reset_triggered:
    #     # ser.write(reset_command)  # Send reset command if the long press condition was met
    #     reset_triggered = False  # Reset the trigger
    # else:
    #     print ("no reset")
    #     # ser.write(no_reset_command)  # Continuously send no reset command if the condition wasn't met

    #         # Read data from serial


        # Read data from serial
    # if ser.in_waiting >= 5:  # Check if at least 5 bytes are available (1 for the flag byte + 4 for the float)
    #         flag_byte = ser.read(1)  # Read the flag byte
    #         if flag_byte == b'\xFF':  # Check if the flag byte is correct (0xFF)
    #             loadcell_bytes = ser.read(4)  # Read the next 4 bytes (float)
    #             received_load = struct.unpack('f', loadcell_bytes)[0]  # Convert bytes to float

    #         if 0.00 <= received_load <= 15.00:  # Validate the received value
    #                 current_load = received_load
    #                 window['-CURRENT-LOAD-'].update(f'{current_load:.2f} kg')  # Update GUI

    #                 # Debugging print statement, you can remove this in production
    #                 print("Received load =", current_load)

        # ... (rest of your event loop)

#    except Exception as e:
#        sg.popup_error(f"An error occurred: {e}")
#        break


window.close()
# ser.close()
