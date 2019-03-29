#二次拟合 公式法
import xlrd
import xlwt
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
workbook=xlrd.open_workbook(r'6.xls')

sheet=workbook.sheet_by_index(0)
cols1=sheet.col_values(0)                          #获取第一列
cols2=sheet.col_values(1)                          #获取第二列
#n为数据规模
n=100
s1=0
s2=0
s3=0
s4=0
s5=0
s6=0
s7=0
#准备变量
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
#等价于
#sp.solve([((s1-b1*s2-b2*s3)/100)-b0,((s4-b0*s2-b2*s5)/s3)-b1,((s6-b0*s3-b1*s5)/s7)-b2],[b0,b1,b2])
#先前答案：
#{b0: 5.54334244651814, b1: 0.458746450400443, b2: 0.960930395945233}
#从结果中提取，根据查找，solve()函数的结果貌似是存储在一个list中的
a=result[b0]
b=result[b1]
c=result[b2]
#绘制散点图
plt.scatter(cols1,cols2,color = 'blue')
#绘制结果图
x=np.linspace(0,15,100)
y=a+b*x+c*x*x
plt.plot(x,y,color="red")
plt.show()
