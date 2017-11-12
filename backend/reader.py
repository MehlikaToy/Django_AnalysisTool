"""
Created on Sun Oct 22 20:18:32 2017

@author: degle
"""

import numpy as np
import pandas as pd


# Loads the matrix and the list of states
# Note: transposing matrix since the states were entered incorrectly
def load_matrix(file, sheet):
    df = pd.read_excel(file, sheetname=sheet)
    return df.values[:,1:].transpose(), df.values[:,0]

# Load variable
def load_var(file, sheet):
    return pd.read_excel(file, sheetname=sheet).values[:,1:]
    

# Clear NaNs
def fill_empty(M):
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
def fill_vars(M, file, age):
    for r in range(len(M)):
        for c in range(len(M[r])):
            if (isinstance(M[r][c], str)):
                var = M[r][c].split()
                var_data = fill_prev(load_var(file, var[0]))
                M[r,c] = var_data[age%len(var_data) ,int(var[1])]
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
def generate_model(file='matrix.xlsx', age=30, female=False):
    if(female):
        age += 100
    matrix, states = load_matrix(file, 'data')
    matrix = fill_vars(matrix, 'matrix.xlsx', age)
    matrix = fill_empty(matrix)
    if(female):
        matrix = female_mod(matrix, file, 'gender')
    matrix = fill_remain(matrix)
    
    return matrix, states
    


'''    
matrix, states = generate_model()
for row in matrix:
    print(list(row))
print(states)
'''