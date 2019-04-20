2019/4/20  
**二层BP神经网络**  
但是仍有部分在公式上的不明了，但是其运作方式还是很简单的，先简单解析我的代码  
`from createData import generate_data`  
是本次所解题目的训练集生成软件，generate_data(N)会返回两个数组，一个为N*100的训练集及其对应的N*1的结果，十分方便  
```
L0=2*np.random.random((100,5))-1
L1=2*np.random.random((5,1))-1
```  
由于本次想构建的是二层神经网络，因此需要两层的计算层，其中我将中间的隐藏层设置为5个神经元，而输出层的表示方法为0.1~0.6的离散数，而不是6个0或1元素的数组，因此输出层为1个神经元(而不是6个)，这样经过矩阵运算后矩阵维度能够与结果相同。  
```
def sigmoid(x):
    return 1/(1+np.exp(-x))
```  
本次使用的激活函数:sigmoid函数，特点为非线性(并不是条直线)，区间在[0,1]上，且没有任何点导数为0(趋近于0的有)，同时他的导数也非常简洁:  
```
def dsigmoid(x):
    return x*(1-x)
```  
因此这一次选择使用这个激活函数。  
  
生成数据:  
```
X,Y=generate_data(50)
X=np.array(X)
Y=np.array(Y)
#shape of parameters
#X(50*100) Y(50*1)
#L0(100*5) L1(5*1)
L0=2*np.random.random((100,5))-1
L1=2*np.random.random((5,1))-1
```  
要谨记转换两数据的形式(List/Array)  
并且标记出来了X,Y,L0,L1,分别的维数方便查看，其中L0,L1的生成方式是产生了填满位于[-1,1]的元素的数组(应该是吧...)
  
主题训练过程:  
```
for i in range(50000):
    #forward
    temp0=X
    temp1=sigmoid(np.dot(temp0,L0))
    temp2=sigmoid(np.dot(temp1,L1))
    error2=Y-temp2
    if (i%5000)==0:
        print(np.mean(error2))
    #backward
    d2=error2*dsigmoid(temp2)
    error1=d2.dot(L1.T)
    d1=error1*dsigmoid(temp1)
    L1+=temp1.T.dot(d2)
    L0+=temp0.T.dot(d1)
```  
整体而言得益于矩阵使得过程十分流畅，内容主要涉及到了不断的求偏导并运用链式法则不断"接近"结果与目标变量的偏导，先不赘述算法了。  
最后的检验部分...应该也不用再讲什么了吧...  
同时由于开始的层元素为随机生成所以每次运行不一定相同，可以用seed()函数解决这个问题  
Test1:  
```
-0.19711045500123067
-5.796510982417874e-05
-2.6806406495373803e-05
-1.2019265739013352e-05
-5.227927664957222e-06
-2.2248997057949804e-06
-9.364114896748266e-07
-3.9213879621080584e-07
-1.6385924452994028e-07
-6.84074828341541e-08
[[0.40000002]
 [0.50000153]]
[[0.4]
 [0.5]]
```  
Test2:  
```
0.16291901475086618
-0.0035140803158310225
1.9674898472920034e-05
2.840084784809016e-05
1.790320520679012e-05
1.059859397264329e-05
5.907123617054088e-06
3.147002414242428e-06
1.6152543191538805e-06
3.5777556424282377e-07
[[0.40004171]
 [0.50000385]]
[[0.4]
 [0.5]]
```  
不过倒是可以看出来挺准确的就是了...  
完整代码如下:  
```
import numpy as np
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

for i in range(50000):
    #forward
    temp0=X
    temp1=sigmoid(np.dot(temp0,L0))
    temp2=sigmoid(np.dot(temp1,L1))

    error2=Y-temp2
    if (i%5000)==0:
        print(np.mean(error2))
    
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
print(t2)
print(Y1)
```
