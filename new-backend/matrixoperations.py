import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt

m = np.array([[0, 1], [-1, 0]])

def iter(m, num):
	return LA.matrix_power(m, num)

def util(cost, m, num):
	sum = 0
	for i in range(1, num, 1):
		sum += cost * LA.matrix_power(m, i)
	return sum

age = 30

plt.scatter([10, 20, 50, 60], [.1, .2, .4, .7] , label='Mortality')
plt.scatter([10, 20, 50, 60], [.9, .8, .6, .3] , label='Cirrhosis')
plt.legend(loc='best')
plt.axis([0, (100 - age), 0, 1])
plt.ylabel('Probability in State')
plt.xlabel('Years Later')
plt.title('Predicted Mortality Rate')
plt.show()

