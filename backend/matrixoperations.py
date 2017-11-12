import numpy as np
from numpy import linalg as LA

m = np.array([[0, 1], [-1, 0]])

def pwr(M, num):
	return LA.matrix_power(M, num)

def util(cost, m, num):
	sum = 0
	for i in range(1, num, 1):
		sum += cost * LA.matrix_power(m, i)
	return sum

age = 30
