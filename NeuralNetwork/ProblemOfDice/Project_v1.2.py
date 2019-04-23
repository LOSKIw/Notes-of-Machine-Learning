import numpy as np
import matplotlib.pyplot as plt
from createData import generate_data
from createData import generate_all

def sigmoid(x):
    return 1/(1+np.exp(-x))

def dsigmoid(x):
    return x*(1-x)
train=100000

X,Y=generate_all()
X=np.array(X)
Y=np.array(Y)

#shape of parameters
#X(50*100) Y(50*1)
#L0(100*5) L1(5*1)

L0=2*np.random.random((100,20))-1
L1=2*np.random.random((20,1))-1
y=[]

for i in range(train):
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

    L1+=temp1.T.dot(d2)*0.1
    L0+=temp0.T.dot(d1)*0.1

'''
X1=np.array(X1)
Y1=np.array(Y1)
t1=sigmoid(np.dot(X1,L0))
t2=sigmoid(np.dot(t1,L1))
'''
plt.subplot(211)
x1=np.linspace(0,train,train)
plt.plot(x1,y)

plt.subplot(212)
testResult=sigmoid(np.dot(sigmoid(np.dot(X,L0)),L1))
test=[]
x2=np.linspace(0,648,648)
count=0
for i in range(testResult.size):
    if(abs(testResult[i][0]-Y[i][0]))<=0.01:
        count+=1
    test.append(count/(i+1))
plt.plot(x2,test)
'''
for i in range(10):
    test = [int(n) for n in input().split()]
    test=np.array(test)
    testend=float(input())

    testResult=sigmoid(np.dot(sigmoid(np.dot(test,L0)),L1))

    print("your",testend)
    print("{:.2f}".format(testResult[0]))
'''
print(L0,L1)
print(count/(i+1))
np.savetxt("C:/Users/59651/Desktop/L0.txt", L0)
np.savetxt("C:/Users/59651/Desktop/L1.txt", L1)
plt.show()
