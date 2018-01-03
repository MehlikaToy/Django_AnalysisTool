"""
loadxl.py
Converts an xl file into an equivalent Python dictionary.
"""

import numpy as np
import pandas as pd


def load_sheet(file, sheet):
    """
    Loads an Excel sheet into a 2d array
    """
    df = pd.read_excel(file, sheetname=sheet)
    return df.values.tolist()


def load_file(file):
    """
    Loads all the Excel sheets into a dictionary.
    """
    data = {}
    
    xl = pd.ExcelFile(file)
    for sheet in xl.sheet_names:
        data[sheet] = load_sheet(file, sheet)
        
    return data


def write_pyfile(file):
    """
    Convert an Excel file to a Python text file.
    """
    data = load_file(file)
    pyfilename = "pydata_" + file.split(".")[0] + ".py"
    
    pyfile = open(pyfilename, 'w')
    pyfile.write("from numpy import *\n")
    pyfile.write("xl = " + str(data))
    pyfile.close()