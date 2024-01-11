import PySimpleGUI as sg
import serial
from PIL import Image
import os


sg.theme('Dark')
background_color = sg.theme_background_color()

# ser = serial.Serial('COM9', 9600)

window_x_position = 100
window_y_position = 100

left_foot_grey_image = 'Lefto.png'
left_foot_color_image = 'Left.png'
right_foot_grey_image = 'Righto.png'
right_foot_color_image = 'Right.png'

is_left_foot_color = False
is_right_foot_color = False

play_button_grey = "play.png"
pause_button_orange = "pause.png"
plus_button_grey = "plus.png"
minus_button_grey = "minus.png"
star_button_grey = "staroff.png"
star_button_orange = "staron.png"

is_playing = False
target_load = 4.0
current_load = 0.0
is_star_active = False

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

resized_logo_path = prepare_logo(company_logo_path, 500, 500)  # Adjust the size as needed

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
        [create_image_button(left_foot_grey_image, '-LEFT-FOOT-', size=(300, 600))],
    ]),
    sg.Column([
        [create_image_button(right_foot_grey_image, '-RIGHT-FOOT-', size=(300, 600))]
    ]),
    sg.Column([
        [sg.Image(filename=resized_logo_path, pad=((logo_x_offset, 0), (logo_y_offset, 0)))],
        [sg.Text("Foot Comfort Technology", pad=((logo_x_offset, 0), (0, 0)), font=("Helvetica", 16))],
        [sg.Text('🎯', font=('Helvetica', 30)), sg.Text(f'{target_load:.1f} kg', key='-TARGET-LOAD-', font=('Helvetica', 20)),
         sg.Text('⚡', font=('Helvetica', 20)),  # Buffer space
         sg.Text(f'{current_load:.1f} kg', key='-CURRENT-LOAD-', font=('Helvetica', 20))],
        [create_image_button(play_button_grey, '-PLAY-PAUSE-', size=(100, 100)),
         create_image_button(plus_button_grey, '-PLUS-', size=(100, 100)),
         create_image_button(minus_button_grey, '-MINUS-', size=(100, 100)),
         create_image_button(star_button_grey, '-STAR-', size=(100, 100))]
    ])]
]

window = sg.Window('Foot Comfort Control', layout, finalize=True, size=(1280, 800), background_color=background_color, location=(window_x_position, window_y_position))

# Event loop and logic for updating buttons
# ...

# Event loop
while True:
    try:
        event, values = window.read()

        current_load += 0.1  # Replace with actual data from the slave
        window['-CURRENT-LOAD-'].update(f'{current_load:.1f} kg')

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

        # Update Left Foot Image
        current_left_image = left_foot_color_image if is_left_foot_color else left_foot_grey_image
        window['-LEFT-FOOT-'].update(image_filename=resize_image(current_left_image, 300, 600))

        # Update Right Foot Image to Grey
        current_right_image = right_foot_grey_image
        window['-RIGHT-FOOT-'].update(image_filename=resize_image(current_right_image, 300, 600))

        # ser.write(b'LeftFootCommand')  # Replace with the actual command for the left foot

        # Toggle Right Foot
    elif event == '-RIGHT-FOOT-':
        is_left_foot_color = False  # Turn the left foot off
        is_right_foot_color = True  # Turn the right foot on

        # Update Right Foot Image
        current_right_image = right_foot_color_image if is_right_foot_color else right_foot_grey_image
        window['-RIGHT-FOOT-'].update(image_filename=resize_image(current_right_image, 300, 600))

        # Update Left Foot Image to Grey
        current_left_image = left_foot_grey_image
        window['-LEFT-FOOT-'].update(image_filename=resize_image(current_left_image, 300, 600))

        # ser.write(b'RightFootCommand')

        # Toggle Play/Pause
    elif event == '-PLAY-PAUSE-':
        is_playing = not is_playing  # Toggle state
        new_image = pause_button_orange if is_playing else play_button_grey
        window['-PLAY-PAUSE-'].update(image_filename=resize_image(new_image, 100, 100))

    elif event == '-PLUS-' and target_load < 20:
        target_load += 0.5
        window['-TARGET-LOAD-'].update(f'{target_load:.2f} kg')
        # ser.write(b'IncreaseLoad')  # Replace with the actual command

    elif event == '-MINUS-' and target_load > 0:
        target_load -= 0.5
        window['-TARGET-LOAD-'].update(f'{target_load:.2f} kg')
        # ser.write(b'DecreaseLoad')  # Replace with the actual command

    # Toggle the star button's state and update its image
    elif event == '-STAR-':
        is_star_active = not is_star_active
        new_image = star_button_orange if is_star_active else star_button_grey
        window['-STAR-'].update(image_filename=resize_image(new_image, 100, 100))
        star_status = b'StarActive' if is_star_active else b'StarInactive'
        # ser.write(star_status)  # Send the star status to the Arduino

window.close()
# ser.close()
