import PySimpleGUI as sg

# Define the layout using a Column with custom placement settings
layout = [
    [sg.Text(' ', size=(10, 1)), sg.Button('Button 1', size=(10, 1), key='-TOPRIGHT-'), sg.Text('', size=(5, 1))],
    [sg.Button('Button 2', size=(10, 1)), sg.Text('', size=(10, 1)), sg.Button('Button 4', size=(10, 1))],
    [sg.Text(' ', size=(5, 1)), sg.Button('Button 5', size=(10, 1)), sg.Text('', size=(5, 1))],
    [sg.Button('Exit')]
]

# Create the window
window = sg.Window('Diamond Layout Example', layout)

# Event loop
while True:
    event, values = window.read()

    # Exit the program if the window is closed or the 'Exit' button is clicked
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

# Close the window
window.close()