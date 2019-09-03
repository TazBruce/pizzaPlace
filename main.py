import PySimpleGUI as sg
import sqlite3

layout = [[sg.Text('Your typed chars appear here:'), sg.Text('', size=(15,1), key='_OUTPUT_')],
          [sg.Input(key='_IN_')],
          [sg.Button('Show'), sg.Button('Exit')]]

window = sg.Window('Window Title', layout)

while True:  # Event Loop
    event, values = window.Read()
    print(event, values)
    if event is None or event == 'Exit':
        break
    if event == 'Show':
        # Update the "output" element to be the value of "input" element
        window.Element('_OUTPUT_').Update(values['_IN_'])

window.Close()