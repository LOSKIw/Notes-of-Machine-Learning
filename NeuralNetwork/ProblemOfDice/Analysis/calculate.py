import numpy as np
import matplotlib.pyplot as plt
from createData import generate_data
from createData import generate_all

def sigmoid(x):
    return 1/(1+np.exp(-x))

X,Y=generate_all()
L0=np.loadtxt("L0.txt")
L1=np.loadtxt("L1.txt")
testResult=sigmoid(np.dot(sigmoid(np.dot(X,L0)),L1))
test=[]
x2=np.linspace(0,648,648)
count=0

for i in range(testResult.size):
    if(abs(testResult[i]-Y[i]))<=0.01:
        count+=1
    test.append(count/(i+1))
plt.plot(x2,test)
print(count/(i+1))

print(L0)
print(L1)
plt.show()
