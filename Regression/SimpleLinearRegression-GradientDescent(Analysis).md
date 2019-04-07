2019/3/25  
**一元线性回归——梯度下降/最小二乘法**_又名：一两位小数点的悲剧_  
  
感觉这个才是真正的重头戏，毕竟前两者都是更倾向于直接使用公式，而不是让计算机一步步去接近真相，而这个梯度下降就不一样了，计算机虽然还是跟从现有语句/公式，但是在不断尝试中一步步接近目的地。  
简单来说，梯度下降的目的在我看来还是要到达两系数的偏导数函数值为零的取值，因此，我们会从“任意一点”开始不断接近，由于根据之前最小二乘法的推导，可以说方差的公式应该算一个二次函数...?总之，这么理解的话就算只用中学知识也能知道在导数值为0时求得最大/小值。  
那么就很简单了，我们让a，b一点点接近就可以了，而逼近的过程十分有趣，且巧妙。当前点的导数值如果为正，说明该点的横坐标需要左移，而为负则需要右移（为0就胜利了），因此根据这个特性我们可以直接设定为以下python代码：
```
a=a-n*get_pa(c,d)
b=b-n*get_pb(c,d)
```  
其中，get_pa()以及get_pb()对应的分别为a或b求偏导数值，以a，b两个值为输入值，而n则是非常重要的调节系数，重要到让我无法正常运行程序，后文会着重提及。  
运用到了正减，负增，通过减法实现，很巧妙【来自于Coursera的华盛顿大学“机器学习：回归”课程的想法  
  
接下来，还是先给出求方差，求偏导的函数。  
求方差：  
```
def get_sqm(a,b):
    sqm=0
    for i in range(100):
        sqm=sqm+(cols2[i]-a-b*cols1[i])*(cols2[i]-a-b*cols1[i])
    return sqm
```  
  
求a,b的偏导：  
```
def get_pa(a,b):
    pa=0
    for i in range(100):
        pa=pa-2*(cols2[i]-a-b*cols1[i])
    return pa
```  
```
def get_pb(a,b):
    pb=0
    for i in range(100):
        pb=pb-2*cols1[i]*(cols2[i]-a-b*cols1[i])
    return pb
```  
  
好像...也没有太多可说的？那就迫不及待的进入正题吧！来自于我被调节系数n折磨的一整个下午的怨念！其实主题的循环函数并不是那么难理解和构建，我很早就完成了：  
```
while abs(get_pa(a,b))>=10 and abs(get_pb(a,b))>=10 :
    c=a
    d=b
    a=a-n*get_pa(c,d)
    b=b-n*get_pb(c,d)
    print(get_sqm(a,b))
```  
偏导数的限制...我取了10...看起来很惊悚，但也是没办法，被吓得，只能松一点了。  
简单来说就是不断调整两个系数取值，而且最终要的，也是我用临时变量c,d的原因，**a,b要同时调整**，或者说，在当前情况下，由于两偏导数都是既有a又有b的，牵一发而动全身，调完一个另一个也有了变化，不再准确，也不是之前的那个对应点的偏导数值了。
同时，n的存在也**非常重要**，它是外部限制调节幅度的方式，而它的取值又非常玄学，没有一个定论......对于不同的数据有不同的措施，在Coursera上建议的0.1把我坑惨了。
使用0.1，最后只会给我两个蓝蓝的“nan”，大概是python中的某一个错误表达吧，反正我一直以为我代码有问题，直到晚上才随手灵机一动，加了几个0，然后——就成功了...  
【太过于戏剧性了，我的焦虑完全一笔带过  
在同时我也打印出当前的方差，若是n取0.0001，则显示出的数据为大约又450多行，象征性的表示一下  
```
59842.51109094548
44733.39899894902
...
27787.81855782964
27787.002777912836
```
能感受到前后变化的差距，最后的a,b值也不错，差别不大【偏导数限制在10好像也没什么大关系...  
  
- 最小二乘法公式法  

    `a=-22.63450339669057  b=13.449314363947979`  

- 梯度下降(n=0.0001,偏导数约束为10)  

    `a=-21.128787257903344  b=13.281329019963474`  

- 梯度下降(n=0.0001,偏导数约束为1)  

    `a=-22.48409512730926  b=13.432534053091723`  

- 梯度下降(n=0.00001,偏导数约束为1)  

    `a=-22.483484868708103  b=13.432465969541052`  

目前来看，下降偏导数约束带来的提升可能比调整系数的下降来的多？不过毕竟直接从10减到了1，幅度比n的变化不知道大了多少。  
n=0.0001，少一个0，就会有俩“nan”看着我，气  
由于图像上的差异并不大所以就用n=0.00001,偏导数约束为1的图像吧，不能让它白跑那么久：  
![Figure_1](https://user-images.githubusercontent.com/48372803/54925168-bb4aec80-4f48-11e9-9fa7-6351e6cfaa16.png)  
  
用的还是这个更像二次的数据，凑合看吧。  
这里给出完整代码：  
```
import xlrd
import xlwt
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
workbook=xlrd.open_workbook(r'1.xls')

sheet=workbook.sheet_by_index(0)
cols1=sheet.col_values(0)   #获取第一列
cols2=sheet.col_values(1)   #获取第二列

#a+bx
#a=sp.Symbol('a')
#b=sp.Symbol('b')
#已知a=-22.63450339669057 b=13.449314363947979

def get_sqm(a,b):
    sqm=0
    for i in range(100):
        sqm=sqm+(cols2[i]-a-b*cols1[i])*(cols2[i]-a-b*cols1[i])
    return sqm

def get_pa(a,b):
    pa=0
    for i in range(100):
        pa=pa-2*(cols2[i]-a-b*cols1[i])
    return pa

def get_pb(a,b):
    pb=0
    for i in range(100):
        pb=pb-2*cols1[i]*(cols2[i]-a-b*cols1[i])
    return pb
n=0.00001
a=0.0
b=0.0
while abs(get_pa(a,b))>=1 and abs(get_pb(a,b))>=1 :
    c=a
    d=b
    a=a-n*get_pa(c,d)
    b=b-n*get_pb(c,d)
    print(get_sqm(a,b))

print(a,b)
plt.scatter(cols1,cols2,color = 'blue')
x=np.linspace(0,15,100)
y=b*x+a
plt.plot(x,y,color="red")
plt.show()
```
就先这样，草草结束了先...?
