"""
reader.py
Reads Excel spreadsheets and loads model data into Python.
"""

import numpy as np
import pydata_em1_nat as e1n
import pydata_em1_trt as e1t

fl_ref = {'e1n':e1n.xl, 'e1t':e1t.xl}

def load_matrix(file, sheet):
    """
    Loads the matrix and the list of states.
    Note: transposing matrix since the states were entered incorrectly.
    """
    data = np.array(fl_ref[file][sheet], dtype='O')
    return data[:,1:].transpose(), data[:,0]


def load_var(file, sheet):
    """
    Loads data for a single variable from the spreadsheet.
    """
    return np.array(fl_ref[file][sheet], dtype='O')[:,1:]
    

def fill_empty(M):
    """
    Clears all the NaNs in the spreadsheet.
    """
    for i in range(len(M)):
        for j in range(len(M[0])):
            if ((not isinstance(M[i,j], str)) and np.isnan(M[i,j])):
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
            if (isinstance(M[r][c], str) and M[r][c] != 'id'):
                var = M[r][c].split()
                var_data = fill_prev(load_var(file, var[0]))
                M[r,c] = var_data[values[var[0]] ,int(var[1])]
    return M


# Enter probabilities of remaining in state
def fill_probs(M):
    for i in range(len(M)):
        M[i][i] = 1 - sum(M[:,i])
    return M


def female_mod(M, file, sheet):
    female, labels = load_matrix(file, sheet)
    
    M_out = M[:,:]
    for r in range(M.shape[0]):
        for c in range(M_out.shape[1]):
            if ( (not isinstance(M[r,c], str)) and female[r,c] == 1):
                M_out[r,c] = M[r,c] * 0.5
    
    return M_out


# TODO
def fill_remain(M, labels):
    for r in range(len(M)):
        for c in range(len(M[0])):
            if (M[r][c] == 'id'):
                M[r][c] = np.nan
                M[r][c] = 1 - np.nansum(M[:,c])
    return M
    

# Putting it all together
def generate_model(female=False, age=30, file='e1n'):
    matrix, states = load_matrix(file, 'data')
    values = {'age':age, 'mort':age+100*female}
    
    matrix = fill_vars(matrix, file, values)
    matrix = fill_empty(matrix)
    if(female):
        matrix = female_mod(matrix, file, 'gender')
    matrix = fill_remain(matrix, states)
    
    return matrix, states
    

