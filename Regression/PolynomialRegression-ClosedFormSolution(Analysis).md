2019/3/25  
真的，当那个图像出现的时候，我真的感觉太美了。  
或许是一路上以来自我的摸索加深的我对于这个模型的感受吧。  
**二次函数拟合——最小二乘法公式法**  
与线性回归相似，对二次函数进行拟合某种意义上也只是加了一个函数，虽然求解的方程变得更加繁琐，需要准备的变量也增加到了七个。  
思路有借鉴于：[最小二乘法拟合二次曲线 C语言](https://blog.csdn.net/frustratd/article/details/80968772)  
为了更好的理解回归问题中最小二乘法的求偏导过程，这次我选择自己手打公式。  
大概流程如下  
![image](https://user-images.githubusercontent.com/48372803/54882826-fd1c5a00-4e98-11e9-979e-1a4ebb9ce7b9.png)  
但是到此处之后便被这三个繁琐的方程给难倒了，虽然肯定可以说是能强解，但是感觉就是不断地消元，还是在大量系数的情况下，于是我查找了资料，自然万能的python库是无所不能的，解三元一次方程这种小事当然轻松——sympy库
这个库简直是神器，我主要运用了一下几个功能  
  
声明变量  
```
b0=sp.Symbol('b0')
b1=sp.Symbol('b1')
b2=sp.Symbol('b2')
```  
毕竟出现在方程中的未知数是未定义的，一般情况下是不能允许定义前的运算，可以说这是解方程的基础。  
  
解方程  
```
f1=((s1-b1*s2-b2*s3)/100)-b0
f2=((s4-b0*s2-b2*s5)/s3)-b1
f3=((s6-b0*s3-b1*s5)/s7)-b2
result=sp.solve([f1,f2,f3],[b0,b1,b2])
```  
或  
`sp.solve([((s1-b1*s2-b2*s3)/100)-b0,((s4-b0*s2-b2*s5)/s3)-b1,((s6-b0*s3-b1*s5)/s7)-b2],[b0,b1,b2])`  
  
然而此处出现了一个巨大的坑，那就是，最终如果这样输出  
`print(sp.solve([f1,f2,f3],[b0,b1,b2]))`  
结果便是  
`{b0: 5.54334244651814, b1: 0.458746450400443, b2: 0.960930395945233}`  
一开始我没有意识到，直到运行时满屏幕红字报错，其中最主要的一句话  
`TypeError: can't convert expression to float`  
我当时就纳了闷了，print结果好好的，都是float，怎么还不行？  
后来不断查阅网上相关博客，直到  
[使用python的sympy解符号方程组后，如何将结果带入之后的符号表达式](https://zhidao.baidu.com/question/1579537023552071340.html)  
真的是，一语点醒梦中人。  
solve得出的解并不是完好的存在了之前“声明”的变量中，严格意义上来讲，是存储在了一个词典中。他的索引是那个变量名。也就是说，我们把变量名当成了字符形式，真正意义上只是个摆设，表示未知量却不存储最终结果，看到这里真是又兴奋有懊悔，或许是我对python的特殊数据类型不熟悉吧。也因此最终用了以下函数解决  
```
a=result[b0]
b=result[b1]
c=result[b2]
```
plt.plot()函数也遇到了这个问题，不过也解决了。  
至此呈上结果图
![Figure_1](https://user-images.githubusercontent.com/48372803/54882768-5df76280-4e98-11e9-8152-ca9ddbc539a6.png)  
或许这就是完成一个小工程的喜悦吧。  

完整代码如下（留有过去删改及笔记）：  
```
import xlrd
import xlwt
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
workbook=xlrd.open_workbook(r'6.xls')

sheet=workbook.sheet_by_index(0)
cols1=sheet.col_values(0)   #获取第一列
cols2=sheet.col_values(1)   #获取第二列
n=100
s1=0
s2=0
s3=0
s4=0
s5=0
s6=0
s7=0
for i in range(n):
    s1=s1+cols2[i]
    s2=s2+cols1[i]
    s3=s3+cols1[i]*cols1[i]
    s4=s4+cols1[i]*cols2[i]
    s5=s5+cols1[i]*cols1[i]*cols1[i]
    s6=s6+cols1[i]*cols1[i]*cols2[i]
    s7=s7+cols1[i]*cols1[i]*cols1[i]*cols1[i]
b0=sp.Symbol('b0')
b1=sp.Symbol('b1')
b2=sp.Symbol('b2')
f1=((s1-b1*s2-b2*s3)/100)-b0
f2=((s4-b0*s2-b2*s5)/s3)-b1
f3=((s6-b0*s3-b1*s5)/s7)-b2
result=sp.solve([f1,f2,f3],[b0,b1,b2])

#{b0: 5.54334244651814, b1: 0.458746450400443, b2: 0.960930395945233}

#b0=sp.Symbol('b0')
#b1=sp.Symbol('b1')
#b2=sp.Symbol('b2')
#sp.solve([((s1-b1*s2-b2*s3)/100)-b0,((s4-b0*s2-b2*s5)/s3)-b1,((s6-b0*s3-b1*s5)/s7)-b2],[b0,b1,b2])
a=result[b0]
b=result[b1]
c=result[b2]
plt.scatter(cols1,cols2,color = 'blue')
x=np.linspace(0,15,100)
y=a+b*x+c*x*x
plt.plot(x,y,color="red")
plt.show()
```
