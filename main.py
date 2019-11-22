import csv
import PySimpleGUI as sg
import pandas as pd
import sys

pizzaList = []
price = 0


def wipetab(tab):
    if tab == 'Create Order':
        window.element("_FIRST_NAME_").Update(value='')
        window.element("_LAST_NAME_").Update(value='')
        window.element('_TOTAL_PIZZA_').Update(values=pizzaList)
        window.element("_ADDRESS_").Update(disabled=True, value='')
        sg.Popup('Order Created!', keep_on_top=True)
    else:
        window.element("_PIZZA_").Update(value='')
        window.element("_PRICE_").Update(value='')
        sg.Popup('Pizza Created!', keep_on_top=True)


# Function that checks what tab the user is on, then deletes the currently selected row on that tab
def deltable():
    try:
        if values['_TAB_GROUP_'] == 'Create Pizza':
            table = pd.read_csv("pizzaList.csv")
            deltable = table.drop(values['_PIZZA_LIST_TABLE_'])
            export_csv = deltable.to_csv(r'pizzaList.csv', index=None, header=True)
            tableupdate(False)
        else:
            table = pd.read_csv("pizzaCustomers.csv")
            delTable = table.drop(values['_ORDER_TABLE_'])
            export_csv = delTable.to_csv(r'pizzaCustomers.csv', index=None, header=True)
            tableupdate(True)
    except:
        sys.exit(0)


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
    if customertable:  # if customertable is equal to True open pizzaCustomers
        with open('pizzaCustomers.csv', "r") as inFile:
            reader = csv.reader(inFile)
            next(reader, None)  # skips header row
            data = list(reader)  # read everything else into a list of rows
            window.element('_ORDER_TABLE_').Update(values=data, num_rows=min(len(data), 20))  # update table on GUI
    else:
        with open('pizzaList.csv', "r") as inFile:
            reader = csv.reader(inFile)
            next(reader, None)
            data = list(reader)  # read everything else into a list of rows
            window.element('_PIZZA_TABLE_').Update(values=data, num_rows=min(len(data), 20))
            window.element('_PIZZA_LIST_TABLE_').Update(values=data, num_rows=min(len(data), 20))


# Function that adds selected order on current table to list which can then update gui
# Also calculates total cost
def addpizza(add, cost):
    if add:
        with open('pizzaList.csv', 'r', newline='') as pizzaFile:
            reader = csv.reader(pizzaFile)
            rows = list(reader)
            rowNum = int(str(values['_PIZZA_TABLE_']).strip('[]'))  # row number selected from table and remove brackets
            rowNum += 1  # skip header row
            pizza = rows[rowNum]
            cost += int(pizza[1])
            pizzaList.append(pizza[0])
            window.element('_TOTAL_PIZZA_').Update(values=pizzaList)
            return cost
    else:
        window.element('_TOTAL_PIZZA_').Update(values=pizzaList)
        return cost


with open('pizzaCustomers.csv', "r") as CustomerTable:
    customerReader = csv.reader(CustomerTable)
    customerHeaderList = next(customerReader)
    customerData = list(customerReader)  # read everything else into a list of rows

with open('pizzaList.csv', "r") as PizzaTable:
    pizzaReader = csv.reader(PizzaTable)
    pizzaHeaderList = next(pizzaReader)
    pizzaData = list(pizzaReader)  # read everything else into a list of rows

sg.ChangeLookAndFeel('Reds')

tab1_layout = [[sg.T('Add Order', font='sfprodisplay 25 bold')],
               [sg.T('First Name', size=(10, 0)), sg.VerticalSeparator(pad=None), sg.Input(size=(20, 0), key="_FIRST_NAME_")],
               [sg.T('Last Name', size=(10, 0)), sg.VerticalSeparator(pad=None), sg.Input(size=(20, 0), key="_LAST_NAME_")],
               [sg.T('Add Pizza', size=(10, 0)), sg.VerticalSeparator(pad=(7, 0)),
                sg.Table(
                    values=pizzaData,
                    headings=pizzaHeaderList,
                    max_col_width=25,
                    auto_size_columns=True,
                    justification='left',
                    num_rows=min(len(pizzaData), 20), key='_PIZZA_TABLE_'), sg.Button('Add', size=(5, 0))],
               [sg.T('Total Pizzas', size=(10, 0)), sg.VerticalSeparator(pad=None),
                sg.Listbox(values=[], size=(17, 0), key="_TOTAL_PIZZA_"),
                sg.Button('Remove', size=(5, 0))],
               [sg.T('Delivery?', size=(10, 0)), sg.VerticalSeparator(pad=None),
                sg.Checkbox('', enable_events=True), sg.T('Total Cost'),
                sg.T('$', key="_COST_", size=(4, 0))],
               [sg.T('Street Address', size=(10, 0)), sg.VerticalSeparator(pad=None),
                sg.Input(size=(20, 0), disabled=True, key="_ADDRESS_")],
               [sg.Button("Confirm")]
               ]
tab2_layout = [[sg.T('Total Orders', font='sfprodisplay 25 bold')],
               [sg.Table(
                   values=customerData,
                   headings=customerHeaderList,
                   max_col_width=25,
                   auto_size_columns=True,
                   justification='left',
                   num_rows=min(len(customerData), 20), key='_ORDER_TABLE_')],
               [sg.Button('Delete')]
               ]
tab3_layout = [[sg.T('Create Pizza', font='sfprodisplay 25 bold')],
               [sg.T('Pizza Name  '), sg.Input(size=(23, 1), key="_PIZZA_")],
               [sg.T('Price            '), sg.Input(size=(23, 1), key="_PRICE_")],
               [sg.Button('Create')],
               [sg.Table(
                   values=pizzaData,
                   headings=pizzaHeaderList,
                   max_col_width=25,
                   auto_size_columns=True,
                   justification='left',
                   num_rows=min(len(pizzaData), 20), key='_PIZZA_LIST_TABLE_')],
               [sg.Button('Cut')]
               ]
layout = [[sg.TabGroup([[sg.Tab('Create Order', tab1_layout),
                         sg.Tab('Total Orders', tab2_layout),
                         sg.Tab('Create Pizza', tab3_layout)]
                        ], key="_TAB_GROUP_", selected_title_color='red', title_color='black', enable_events=True)]]

window = sg.Window('pizzaPlace', layout, default_element_size=(20, 1))

while True:
    event, values = window.Read()
    print(values)
    if event == 'Confirm':
        with open('pizzaCustomers.csv', "a", newline='') as newFile:
            writer = csv.writer(newFile)
            if values[0]:
                delivery = 'Yes'
            else:
                delivery = 'No'
            writer.writerow([values['_FIRST_NAME_'], values['_LAST_NAME_'], str(pizzaList).strip('[]'), delivery,
                             str(values['_ADDRESS_']).strip('[,]'), price])
        tableupdate(True)
        pizzaList = []
        wipetab(str(values['_TAB_GROUP_']))
    elif event == 'Create':
        with open('pizzaList.csv', 'a', newline='') as pizzaFile:
            writer = csv.writer(pizzaFile)
            writer.writerow([values["_PIZZA_"], values["_PRICE_"]])
        tableupdate(False)
        wipetab(str(values['_TAB_GROUP_']))
    elif event == 'Add':
        price = addpizza(True, price)
        print(price)
        window.element("_COST_").Update(value=price)
    elif event == 'Remove':
        pizzaList = []
        price = addpizza(False, 0)
        window.element("_COST_").Update(value=price)
    elif event == 'Delete' or 'Cut':
        deltable()
    elif event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break

    # enables address section depending on delivery checkbox being ticked
    if values[0]:
        window.element('_ADDRESS_').Update(disabled=False)
    elif not values[0]:
        window.element('_ADDRESS_').Update(disabled=True)
window.close()

# valuecheck(variable,True = String/False = Integer,minimum,maximum)
