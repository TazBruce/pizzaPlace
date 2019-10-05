import csv

import PySimpleGUI as sg

filename = 'PizzaPlace/pizzaCustomers.csv'
# --- populate table with file contents --- #
data = []
header_list = []
with open(filename, "r+") as infile:
    reader = csv.reader(infile)
    header_list = next(reader)
    data = list(reader)  # read everything else into a list of rows

sg.ChangeLookAndFeel('Reds')

tab1_layout = [[sg.T('Add Order', font='sfprodisplay 25 bold')],
               [sg.T('First Name  '), sg.Input(size=(23, 1))],
               [sg.T('Last Name  '), sg.Input(size=(23, 1))],
               [sg.T('Add Pizza   '), sg.InputCombo(('Ham & Cheese', 'Cheese'), size=(20, 1)), sg.Button('Add')],
               [sg.T('Total Pizzas'), sg.InputCombo('Cheese', size=(20, 1)), sg.Button('Delete')],
               [sg.T('Delivery?    '), sg.Checkbox(''), sg.T('Total Cost'), sg.T('$')],
               [sg.Button("Confirm")]
               ]
tab2_layout = [[sg.Table(values=data,
                         headings=header_list,
                         max_col_width=25,
                         auto_size_columns=True,
                         justification='right',
                         alternating_row_color='lightblue',
                         num_rows=min(len(data), 20))]
               ]
tab3_layout = [[sg.T('Create Pizza', font='sfprodisplay 25 bold')],
               [sg.T('Pizza Name  '), sg.Input(size=(23, 1))],
               [sg.T('Size             '), sg.InputCombo(('Small', 'Medium', 'Large'))],
               [sg.T('Price            '), sg.Input(size=(23, 1))],
               [sg.Button('Confirm')]
               ]
layout = [[sg.TabGroup([[sg.Tab('Create Order', tab1_layout),
                         sg.Tab('View Orders', tab2_layout),
                         sg.Tab('Create Pizza', tab3_layout)]
                        ], selected_title_color='red', title_color='black')]]

window = sg.Window('pizzaPlace', layout, default_element_size=(20, 1))

event, values = window.Read()

while True:
    event, values = window.Read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break

window.close()

# valuecheck(variable,True = String/False = Integer,minimum,maximum)
