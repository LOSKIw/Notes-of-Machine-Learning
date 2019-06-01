import numpy as np
import matplotlib.pyplot as plt

def getLine(x1,x2,a=0):
    print(x1,x2)
    if(x2[0]==x1[0]):
        k=0
    elif(x2[1]==x1[1]):
        k=99999
    else:
        k=-1/ ( (x2[1]-x1[1]) / (x2[0]-x1[0]) )
    b=(x2[1]+x1[1])/2-k*(x2[0]+x1[0])/2
    if(a==1):
        x=np.linspace(0,10,50)
        plt.plot(x,k*x+b,color="yellow")
    return k,b

X1=np.array([[2,1],
            [3,1],
            [4,3]])

X2=np.array([[1,4],
            [3,8],
            [6,20]])

result=dict(k=0,b=0,c=[],d=[])
distance=0
for i1 in X1:
        distance+=(result['k']*i1[0]+result['b']-i1[1])/((result['k']**2+1)**0.5)
            
for j1 in X2:
        distance+=-(result['k']*j1[0]+result['b']-j1[1])/((result['k']**2+1)**0.5)

for i in X1:
    for j in X2:
        sum=0
        k,b=getLine(i,j)
        for i1 in X1:
            if((i1==i).all()):
                continue
            sum+=(k*i1[0]+b-i1[1])/((k**2+1)**0.5)
            
        for j1 in X2:
            if((j1==j).all()):
                continue
            sum+=-(k*j1[0]+b-j1[1])/((k**2+1)**0.5)
        print(sum)
        if sum<distance:
            distance=sum
            result['k']=k
            result['b']=b
            result['c']=i
            result['d']=j

print(result['k'],result['b'],result['c'],result['d'])
plt.scatter(X1[:,0],X1[:,1],color = 'blue')
plt.scatter(X2[:,0],X2[:,1],color = 'red')

x=np.linspace(0,10,50)
plt.plot(x,result['k']*x+result['b'],color="green")
plt.show()
