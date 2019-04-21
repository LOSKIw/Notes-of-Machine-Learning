import numpy as np
import matplotlib.pyplot as plt
from createData import generate_data

def sigmoid(x):
    return 1/(1+np.exp(-x))

def dsigmoid(x):
    return x*(1-x)

X,Y=generate_data(50)
X=np.array(X)
Y=np.array(Y)

#shape of parameters
#X(50*100) Y(50*1)
#L0(100*5) L1(5*1)

L0=2*np.random.random((100,5))-1
L1=2*np.random.random((5,1))-1
y=[]
for i in range(50000):
    #forward
    count=0
    temp0=X
    temp1=sigmoid(np.dot(temp0,L0))
    temp2=sigmoid(np.dot(temp1,L1))

    error2=Y-temp2
    if (i%5000)==0:
        print(np.mean(error2))
    for i in range(Y.size):
        if(abs(temp2[i][0]-Y[i][0]))<=0.001:
           count +=1
    y.append(count/Y.size)
    #backward
    d2=error2*dsigmoid(temp2)
    error1=d2.dot(L1.T)
    d1=error1*dsigmoid(temp1)

    L1+=temp1.T.dot(d2)
    L0+=temp0.T.dot(d1)

X1,Y1=generate_data(2)
X1=np.array(X1)
Y1=np.array(Y1)
t1=sigmoid(np.dot(X1,L0))
t2=sigmoid(np.dot(t1,L1))
x=np.linspace(0,50000,50000)
plt.plot(x,y)
plt.show()
print(t2)
print(Y1)
