import PySimpleGUI as sg

tab1_layout = [[sg.T('Add order')],
               [sg.T('First Name  '), sg.Input(size=(23, 1))],
               [sg.T('Last Name  '), sg.Input(size=(23, 1))],
               [sg.T('Add Pizza   '), sg.InputCombo(('Ham & Cheese', 'Cheese'), size=(20, 1)), sg.Button('Add')],
               [sg.T('Total Pizzas'), sg.InputCombo('Cheese', size=(20, 1)), sg.Button('Delete')],
               [sg.T('Delivery?    '), sg.Checkbox('YES'), sg.T('Total Cost'), sg.T('$')]
               ]

tab2_layout = [[sg.T('This is inside tab 2')],
               [sg.In(key='in')]]

layout = [[sg.TabGroup([[sg.Tab('Create Order', tab1_layout), sg.Tab('Tab 2', tab2_layout)]])],
          [sg.Button('Read')]]

window = sg.Window('My window with tabs', layout, default_element_size=(12, 1))

while True:
    event, values = window.Read()
    print(event, values)
    if event is None:  # always,  always give a way out!
        break
