"""
reader.py
Reads Excel spreadsheets and loads model data into Python.
"""

import numpy as np

from pydata_matrix import xl


def load_matrix(file, sheet):
    """
    Loads the matrix and the list of states.
    Note: transposing matrix since the states were entered incorrectly.
    """
    data = np.array(xl[sheet], dtype='O')
    return data[:,1:].transpose(), data[:,0]


def load_var(sheet, file='matrix.xlsx'):
    """
    Loads data for a single variable from the spreadsheet.
    """
    return np.array(xl[sheet], dtype='O')[:,1:]
    

def fill_empty(M):
    """
    Clears all the NaNs in the spreadsheet.
    """
    for i in range(len(M)):
        for j in range(len(M[0])):
            if (np.isnan(M[i,j])):
                M[i][j] = 0
    return M


# Fill with previous
def fill_prev(M):
    for c in range(len(M[0])):
        for r in range(len(M)):
            if (np.isnan(M[r,c])):
                M[r,c] = M[r-1,c]
    return M


# Fill vars
def fill_vars(M, file, values):
    m,n = M.shape
    for r in range(m):
        for c in range(n):
            if (isinstance(M[r][c], str)):
                var = M[r][c].split()
                var_data = fill_prev(load_var(var[0], file))
                M[r,c] = var_data[values[var[0]] ,int(var[1])]
    return M


# Enter probabilities of remaining in state
def fill_probs(M):
    for i in range(len(M)):
        M[i][i] = 1 - sum(M[:,i])
    return M


def female_mod(M, file, sheet):
    female = load_matrix(file, sheet) * (1/2)
    return np.multiply(M, female)


def fill_remain(M):
    for c in range(len(M[0])):
        M[c,c] = 1 - sum(M[:,c])
    return M
    

# Putting it all together
def generate_model(file='./matrix.xlsx', female=False,
                   age=30, cirr_year=1, trans_year=1):
    if(female):
        age += 100
    matrix, states = load_matrix(file, 'data')
    values = {'age':age, 'cirr_year':cirr_year, 
              'trans_year':trans_year, 'mort':age+100*female}
    
    matrix = fill_vars(matrix, file, values)
    matrix = fill_empty(matrix)
    if(female):
        matrix = female_mod(matrix, file, 'gender')
    matrix = fill_remain(matrix)
    
    return matrix, states
    

