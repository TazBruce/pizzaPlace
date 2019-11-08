import csv

import PySimpleGUI as sg


# Function that checks value for set parameters
def valuecheck(value, string, minimum, maximum):
    # If 'string' parameter is set to True test for character count
    if string:
        try:
            # If string character count is between set range accept value
            if minimum <= len(value) <= maximum:
                print("ACCEPT STRING")
            else:
                print("POPUP")
        # If function fails to test character count value is invalid
        except:
            print("BREAK")
    # If 'string' parameter is set to False test that integer is between range
    else:
        try:
            if minimum <= value <= maximum:
                print("ACCEPT NUMBER")
            else:
                print("POPUP")
        # If function fails to test value is between integer range value is invalid
        except:
            print("BREAK")


# Function that refreshes customer order table
def tableupdate(customertable):
    if customertable:
        with open('pizzaCustomers.csv', "r") as inFile:
            reader = csv.reader(inFile)
            next(reader, None)  # skips
            data = list(reader)  # read everything else into a list of rows
            window.element('_ORDER_TABLE_').Update(values=data, num_rows=min(len(data), 20))
    else:
        with open('pizzaList.csv', "r") as inFile:
            reader = csv.reader(inFile)
            next(reader, None)
            data = list(reader)  # read everything else into a list of rows
            window.element('_PIZZA_TABLE_').Update(values=data, num_rows=min(len(data), 20))


with open('pizzaCustomers.csv', "r") as CustomerTable:
    customerReader = csv.reader(CustomerTable)
    customerHeaderList = next(customerReader)
    customerData = list(customerReader)  # read everything else into a list of rows

with open('pizzaList.csv', "r") as PizzaTable:
    pizzaReader = csv.reader(PizzaTable)
    pizzaHeaderList = next(pizzaReader)
    pizzaData = list(pizzaReader)  # read everything else into a list of rows

# sg.ChangeLookAndFeel('Reds')

tab1_layout = [[sg.T('Add Order', font='sfprodisplay 25 bold')],
               [sg.T('First Name', size=(10, 0)), sg.VerticalSeparator(pad=None), sg.Input(size=(20, 0))],
               [sg.T('Last Name', size=(10, 0)), sg.VerticalSeparator(pad=None), sg.Input(size=(20, 0))],
               [sg.T('Add Pizza', size=(10, 0)), sg.VerticalSeparator(pad=None),
                sg.Combo(('Ham & Cheese', 'Cheese'), size=(17, 0)), sg.Button('Add', size=(5, 0))],
               [sg.T('Total Pizzas', size=(10, 0)), sg.VerticalSeparator(pad=None), sg.Combo("X", size=(17, 0)),
                sg.Button('Delete', size=(5, 0))],
               [sg.T('Delivery?', size=(10, 0)), sg.VerticalSeparator(pad=None), sg.Checkbox(''), sg.T('Total Cost'),
                sg.T('$')],
               [sg.Button("Confirm")]
               ]
tab2_layout = [[sg.T('Total Orders', font='sfprodisplay 25 bold')],
               [sg.Table(
                   values=customerData,
                   headings=customerHeaderList,
                   max_col_width=25,
                   auto_size_columns=True,
                   justification='right',
                   alternating_row_color='lightblue',
                   num_rows=min(len(customerData), 20), key='_ORDER_TABLE_')]
               ]
tab3_layout = [[sg.T('Create Pizza', font='sfprodisplay 25 bold')],
               [sg.T('Pizza Name  '), sg.Input(size=(23, 1))],
               [sg.T('Price            '), sg.Input(size=(23, 1))],
               [sg.Button('Create')],
               [sg.Table(
                   values=pizzaData,
                   headings=pizzaHeaderList,
                   max_col_width=25,
                   auto_size_columns=True,
                   justification='right',
                   alternating_row_color='lightblue',
                   num_rows=min(len(pizzaData), 20), key='_PIZZA_TABLE_')]
               ]
layout = [[sg.TabGroup([[sg.Tab('Create Order', tab1_layout),
                         sg.Tab('View Orders', tab2_layout),
                         sg.Tab('Create Pizza', tab3_layout)]
                        ], selected_title_color='red', title_color='black')]]

window = sg.Window('pizzaPlace', layout, default_element_size=(20, 1))

event, values = window.Read()
while True:
    event, values = window.Read()
    print(values)
    if event == 'Confirm':
        with open('pizzaCustomers.csv', "a", newline='') as newFile:
            writer = csv.writer(newFile)
            writer.writerow([values[0], values[1], values[2], values[4]])
            tableupdate(True)
    elif event == 'Create':
        print("Created")
        with open(r'pizzaList.csv', 'a', newline='') as pizzaFile:
            writer = csv.writer(pizzaFile)
            writer.writerow([values[5], values[6]])
            tableupdate(False)
    elif event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break

window.close()

# valuecheck(variable,True = String/False = Integer,minimum,maximum)
