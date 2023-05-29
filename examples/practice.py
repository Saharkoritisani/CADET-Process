import numpy as np
from scipy.optimize import minimize

#def rosen(x):
#    """The Rosenbrock function"""
#    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)

input = np.linspace(-5,5)
def simulation(a):
    return a * input **2

TRUE_VAL_A = 4
output = simulation(TRUE_VAL_A)

def loss(x):
   abs_vec = abs(output - simulation(x))
   abs_loss = np.sum(abs_vec)
   return abs_loss

#import matplotlib.pyplot as plt
#plt.plot(input, output)
#plt.show()
x0 = 0
res = minimize(loss, x0, method='nelder-mead',
               options={'xatol': 1e-8, 'disp': True})
print(res.x)