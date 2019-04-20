import matplotlib.pyplot as plt
import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

plt.title("sigmoid(x)")

def ReLU(x):
    return np.maximum(x,0)

x=np.linspace(-10,10,10000)
plt.axis([-10, 10, -0, 1]) 
plt.plot(x,sigmoid(x),color="red")

plt.grid()
plt.show()
