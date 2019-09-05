#!/usr/bin/env python
import sys

import PySimpleGUI as sg
import pandas as pd


def table():
    sg.SetOptions(auto_size_buttons=True)
    df = pd.read_csv('pizzaList.csv', sep=',', engine='python', header=None)
    # Header=None means you directly pass the columns names to the dataframe
    header_list = df.iloc[0].tolist()
    # Uses the first row (which should be column names) as columns names
    data = df[1:].values.tolist()
    # Drops the first row in the table (otherwise the header names and the first row will be the same)
    layout = [[sg.Table(values=data, headings=header_list, display_row_numbers=True,
                        auto_size_columns=True, num_rows=min(25, len(data)))]]

    window = sg.Window('Table', grab_anywhere=False)
    event, values = window.Layout(layout).Read()

    sys.exit(69)


table()
