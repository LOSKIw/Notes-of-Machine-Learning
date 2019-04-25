import random
import numpy as np
import matplotlib.pyplot as plt
from createData import generate_data
from createData import generate_all

def sigmoid(x):
    return 1/(1+np.exp(-x))

def dsigmoid(x):
    return x*(1-x)


class BPNN:
    def __init__(self,num=4,step=0.1):
        random.seed(0)
        self.layer={}
        self.layer['X'],self.layer['Y']=generate_all()
        self.layer['X']=np.array(self.layer['X'])
        self.layer['Y']=np.array(self.layer['Y'])
        self.layer['L0']=2*np.random.random((100,num))-1
        self.layer['L1']=2*np.random.random((num,1))-1
        self.step=step
        self.num=num

    def foward(self):
        self.layer['result']=sigmoid(np.dot(sigmoid(np.dot(self.layer['X'],self.layer['L0'])),self.layer['L1']))

    def backward(self):
        error2=self.layer['Y']-self.layer['result']
        d2=error2*dsigmoid(self.layer['result'])
        error1=d2.dot(self.layer['L1'].T)
        d1=error1*dsigmoid(sigmoid(np.dot(self.layer['X'],self.layer['L0'])))
        self.layer['L1'] += sigmoid(np.dot(self.layer['X'],self.layer['L0'])).T.dot(d2)*self.step
        self.layer['L0'] += self.layer['X'].T.dot(d1)*self.step
        
    def display(self):
        print("L0:",self.layer['L0'])
        print("L1:",self.layer['L1'])

    def save(self):
        np.savetxt("C:/Users/59651/Desktop/L0.txt", self.layer['L0'])
        np.savetxt("C:/Users/59651/Desktop/L1.txt", self.layer['L1'])

    def outputrate(self,func=0):
        count=0
        for i in range(self.layer['Y'].size):
            #round(self.layer['Y'][i]*10)/10.0!=self.layer['result'][i]
            if(abs(self.layer['Y'][i]-self.layer['result'][i])<=0.1):
                count+=1
        if func==1:
            print(count/648)
        return count/648
    
    def error(self,num,step):
        total=0
        for i in range(self.layer['Y'].size):
            total+=(self.layer['Y'][i]-self.layer['result'][i])**2
        if(num%step==0):
            print(total)

    def counte(self):
        total=0
        for i in range(self.layer['Y'].size):
            if(abs(self.layer['Y'][i]-self.layer['result'][i])>=0.1):
                total+=1
        return total

if __name__ == '__main__':
    NN=BPNN()
    y=[]
    '''
    #calculate by iteration times
    for i in range(50000):
        NN.foward()
        NN.backward()
        NN.error(num=i,step=1000)
        y.append(NN.outputrate())
    '''
    e=0
    i=0
    flag=0
    temp=0
    #calculate by accuracy
    while(e<0.99):
        NN.foward()
        NN.backward()
        NN.error(num=i,step=1000)
        y.append(NN.outputrate())
        if(i%1000==0):
            NN.outputrate(func=1)
        e=NN.outputrate()
        if(e<=temp):
            flag+=1
        else:
            flag=0
            temp=e
        if(flag>=10000):
            if(e>0.96):
                break
        i+=1
    NN.outputrate(func=1)
    
    NN.save()
    #plt.subplot(211)
    x1=np.linspace(1,i+1,i+1)
    plt.plot(x1,y)
    
    plt.show()
