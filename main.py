import csv
import PySimpleGUI as sg
import pandas as pd
import sys
import numpy as np

pizzaList = []
price = 0
shipping = False
pizzaChoices = 0
confirm = ""
receipt = []


#  rounds number to 4.sf
def roundup(x):
    return float(np.format_float_positional(x, precision=4, unique=False, fractional=False, trim='k'))


# Function that wipes entire 'Create Order' and 'Create Pizza' tab once user has confirmed
def wipetab(tab):
    if tab == 'Create Order':
        window.element("_FIRST_NAME_").Update(value='')
        window.element("_LAST_NAME_").Update(value='')
        window.element("_CONTACT_").Update(value='')
        window.element('_TOTAL_PIZZA_').Update(values=pizzaList)
        window.element("_ADDRESS_").Update(value='')
        sg.Popup('Order Created!', keep_on_top=True, auto_close=True, auto_close_duration=1)
    else:
        window.element("_PIZZA_").Update(value='')
        window.element("_PRICE_").Update(value='')
        sg.Popup('Pizza Created!', keep_on_top=True, auto_close=True, auto_close_duration=1)


# Function that checks what tab the user is on, then deletes the currently selected row on that tab
def deltable():
    # if tab variable is empty (most likely due to window closing) end program
    try:
        # if user on 'Create Pizza' tab
        if values['_TAB_GROUP_'] == 'Create Pizza':
            # pandas module reads csv file
            table = pd.read_csv("pizzaList.csv")
            numrows = len(table)
            if numrows < 2:
                sg.PopupOK("You must have one row at all times!",
                           keep_on_top=True, auto_close=True, auto_close_duration=1)
            else:
                # variable is set to table but without the currently selected entry
                deltable = table.drop(values['_PIZZA_LIST_TABLE_'])
                # overwrite pizzaList with new table
                export_csv = deltable.to_csv(r'pizzaList.csv', index=None, header=True)
                tableupdate(False)
                sg.Popup("Successfully deleted!", keep_on_top=True, auto_close=True, auto_close_duration=0.5)
        else:
            table = pd.read_csv("pizzaCustomers.csv")
            numrows = len(table)
            if numrows < 2:
                sg.PopupOK("You must have one row at all times!",
                           keep_on_top=True, auto_close=True, auto_close_duration=1)
            else:
                delTable = table.drop(values['_ORDER_TABLE_'])
                export_csv = delTable.to_csv(r'pizzaCustomers.csv', index=None, header=True)
                tableupdate(True)
                sg.popup("Successfully deleted!", keep_on_top=True, auto_close=True, auto_close_duration=0.5)
    except:
        sys.exit(0)


# Function that checks value for set parameters
def valuecheck(value, string, minimum, maximum):
    # If 'string' parameter is set to True test for character count
    if string:
        try:
            isnum = float(value)
            return False
        except:
            try:
                # If string character count is between set range accept value
                if minimum <= len(value) <= maximum:
                    print("pass string length")
                    return True
                else:
                    print("fail string length")
                    return False
            # If function fails to test character count value is invalid
            except:
                print("fail string")
                return False
    # If 'string' parameter is set to False test that integer is between range
    else:
        try:
            isnum = float(value)
            if minimum <= len(value) <= maximum:
                print("pass int length")
                return True
            else:
                print("fail int length")
                return False
        # If function fails to test value is between integer range value is invalid
        except:
            print("fail int")
            return False


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
# v2.0 update - added selective deletion for chosen pizzas
def addpizza(add, cost):
    # if no pizza is selected in table prevent crash
    try:
        with open('pizzaList.csv', 'r', newline='') as pizzaFile:
            reader = csv.reader(pizzaFile)
            rows = list(reader)
            if add:
                rowNum = int(str(values['_PIZZA_TABLE_']).strip('[]'))  # row number selected and remove brackets
                rowNum += 1  # skip header row
                pizza = rows[rowNum]
                cost += float((pizza[1]).strip("$"))  # adds cost of selected row to cost variable
                pizzaList.append(pizza[0])  # append pizza of selected row to pizza list variable
                receipt.append([pizza[0], pizza[1]])
                window.element('_TOTAL_PIZZA_').Update(values=pizzaList)  # update GUI list with new variable
                return cost
            else:
                if not values["_TOTAL_PIZZA_"]:  # if no pizza is selected
                    return cost
                else:
                    for row in rows:  # for every row in the rows list
                        if (str(values['_TOTAL_PIZZA_']).strip("['']")) == row[0]:  # if pizza is equal to rows pizza
                            pizza = row[1]  # pizza is made equal to cost of current row
                    cost -= float(pizza.strip("$"))
                    pizzaList.remove(str(values['_TOTAL_PIZZA_']).strip("['']"))  # removes selected pizza by string
                    window.element('_TOTAL_PIZZA_').Update(values=pizzaList)
                    return cost
    except:
        return cost


with open('pizzaCustomers.csv', "r") as CustomerTable:
    customerReader = csv.reader(CustomerTable)
    customerHeaderList = next(customerReader)
    customerData = list(customerReader)  # read everything else into a list of rows
    if not customerData:
        customerData = [['', '', '', '', '', '', '']]


with open('pizzaList.csv', "r") as PizzaTable:
    pizzaReader = csv.reader(PizzaTable)
    pizzaHeaderList = next(pizzaReader)
    pizzaData = list(pizzaReader)  # read everything else into a list of rows
    if not pizzaData:
        pizzaData = [['          ', '   ']]

sg.ChangeLookAndFeel('Reds')

tab1_layout = [[sg.T('Add Order', font='sfprodisplay 25 bold')],
               [sg.T('First Name', size=(10, 0)), sg.VerticalSeparator(pad=None),
                sg.Input(size=(20, 0), key="_FIRST_NAME_", tooltip="Allows 3 to 15 Characters")],
               [sg.T('Last Name', size=(10, 0)), sg.VerticalSeparator(pad=None),
                sg.Input(size=(20, 0), key="_LAST_NAME_", tooltip="Allows 3 to 15 Characters")],
               [sg.T('Phone Number', size=(10, 0)), sg.VerticalSeparator(pad=None),
                sg.Input(size=(20, 0), key="_CONTACT_", tooltip="Allows 8 to 10 Numbers")],
               [sg.T('Add Pizza', size=(10, 0)), sg.VerticalSeparator(pad=(7, 0)),
                sg.Table(
                    values=pizzaData,
                    headings=pizzaHeaderList,
                    auto_size_columns=False,
                    justification='left',
                    num_rows=min(len(pizzaData), 20), key='_PIZZA_TABLE_'), sg.Button('Add', size=(5, 0))],
               [sg.T('Total Pizzas', size=(10, 0)), sg.VerticalSeparator(pad=None),
                sg.Listbox(values=[], size=(17, 0), key="_TOTAL_PIZZA_", enable_events=True),
                sg.Button('Remove', size=(5, 0))],
               [sg.T('Delivery?', size=(10, 0)), sg.VerticalSeparator(pad=None),
                sg.Checkbox('', enable_events=True)],
               [sg.T('Street Address', size=(10, 0)), sg.VerticalSeparator(pad=None),
                sg.Input(size=(20, 0), disabled=True, key="_ADDRESS_")],
               [sg.T('Receipt?', size=(10, 0)), sg.VerticalSeparator(pad=None), sg.Checkbox('', enable_events=True)],
               [sg.T('Total Cost', size=(10, 0)), sg.VerticalSeparator(pad=None), sg.T('$0', key="_COST_", size=(5, 0)), sg.Button("Confirm")]
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
               [sg.T('Pizza', size=(6, 0)), sg.Input(size=(15, 0), key="_PIZZA_", tooltip="Allows 4 to 15 Characters")],
               [sg.T('Price', size=(6, 0)), sg.Input(size=(15, 0), key="_PRICE_", tooltip="Allows 1 to 3 Numbers")],
               [sg.Button('Create')],
               [sg.Table(
                   values=pizzaData,
                   headings=pizzaHeaderList,
                   auto_size_columns=True,
                   justification='left',
                   num_rows=min(len(pizzaData), 20), key='_PIZZA_LIST_TABLE_')],
               [sg.Button('Cut')]
               ]
layout = [[sg.TabGroup([[sg.Tab('Create Order', tab1_layout),
                         sg.Tab('Total Orders', tab2_layout),
                         sg.Tab('Create Pizza', tab3_layout)]
                        ], key="_TAB_GROUP_", selected_title_color='red', title_color='black', enable_events=True)]]

window = sg.Window('pizzaPlace', layout, default_element_size=(20, 1), resizable=True,).finalize()

while True:
    event, values = window.Read()
    print(values)
    if event == 'Confirm':
        test1 = valuecheck(values['_FIRST_NAME_'], True, 3, 15)
        test2 = valuecheck(values['_LAST_NAME_'], True, 3, 15)
        test3 = valuecheck(values["_CONTACT_"], False, 8, 10)
        if test1 and test2 and test3:
            with open('pizzaCustomers.csv', "a", newline='') as newFile:
                writer = csv.writer(newFile)
                if values[0]:
                    delivery = 'Yes'
                else:
                    delivery = 'No'
                writer.writerow([values['_FIRST_NAME_'], values['_LAST_NAME_'], values["_CONTACT_"],
                                 str(pizzaList).strip('[]'),
                                 delivery, str(values['_ADDRESS_']).strip('[,]'), ("$"+str(price))])
            tableupdate(True)
            if values[1]:
                sg.Popup(('''Total Ordered Pizzas and Prices for {}
''' + (str(receipt)) + '''
''' + ("Delivery Charge of 6.99" if values[0] else ("Total Cost of "+str(price)))+'''
''' + (("Total Cost of $"+str(price)) if values[0] else "")
                          ).format(values['_FIRST_NAME_']+" "+values['_LAST_NAME_']+":"))
            pizzaList = []
            if values[0]:
                price = 6.99
            else:
                price = 0
            window.element("_COST_").Update(value=("$"+str(price)))
            wipetab(str(values['_TAB_GROUP_']))
            pizzaChoices = 0
        else:
            sg.Popup("Failed to create order! Make sure your entries are the right length and type.",
                     keep_on_top=True, auto_close=True, auto_close_duration=3)
    elif event == 'Create':
        test1 = valuecheck(values['_PIZZA_'], True, 4, 15)
        test2 = valuecheck(values['_PRICE_'], False, 1, 4)
        if test1 and test2:
            with open('pizzaList.csv', 'a', newline='') as pizzaFile:
                writer = csv.writer(pizzaFile)
                pizzaCost = float(values["_PRICE_"])
                writer.writerow([values["_PIZZA_"], ("$"+str(pizzaCost))])
            tableupdate(False)
            wipetab(str(values['_TAB_GROUP_']))
        else:
            sg.popup("Failed to create pizza! Make sure your entries are the right length and type.",
                     keep_on_top=True, auto_close=True, auto_close_duration=3)
    elif event == 'Add':
        if pizzaChoices < 5:
            price = addpizza(True, price)
            price = roundup(price)
            print(receipt)
            if price > 0:
                pizzaChoices += 1
                window.element("_COST_").Update(value=("$" + str(price)))
        else:
            sg.popup("Too many pizzas have been selected!", keep_on_top=True, auto_close=True, auto_close_duration=1)
    elif event == 'Remove':
        if pizzaChoices > 0:
            price = addpizza(False, price)
            price = roundup(price)
            pizzaChoices -= 1
            window.element('_COST_').Update(value=("$"+str(price)))
        else:
            sg.popup("There are currently no selected pizzas!",
                     keep_on_top=True, auto_close=True, auto_close_duration=1, )
    elif event == 'Delete' or event == 'Cut':
        confirm = sg.popup_ok_cancel('Are you sure you want to remove this entry?', keep_on_top=True)
        if confirm == "OK":
            deltable()
    elif event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    # enables address section depending on delivery checkbox being ticked
    # Also updates cost depending on delivery checkbox
    if values[0]:
        charge = 6.99
        if not shipping:
            shipping = True
            price += charge
            price = roundup(price)
            window.element('_ADDRESS_').Update(disabled=False)
            window.element('_COST_').Update(value=("$" + str(price)))
    else:
        if shipping:
            price -= charge
            shipping = False
        price = roundup(price)
        window.element('_ADDRESS_').Update(disabled=True)
        window.element('_COST_').Update(value=("$" + str(price)))
window.close()
