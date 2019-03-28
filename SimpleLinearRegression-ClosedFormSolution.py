import xlrd
import xlwt
import matplotlib.pyplot as plt           #数学库
import numpy as np                        #数学库
workbook=xlrd.open_workbook(r'1.xls')

sheet=workbook.sheet_by_index(0)
cols1=sheet.col_values(0)                 #获取第一列
cols2=sheet.col_values(1)                 #获取第二列

#plt.plot(cols1,cols2)

#准备变量
n=100
s1=0
s2=0
s3=0
s4=0

#准备所要用的量
for i in range(n):
	s1 = s1 + cols1[i]*cols2[i]
	s2 = s2 + cols1[i]
	s3 = s3 + cols2[i]
	s4 = s4 + cols1[i]*cols1[i]

b = (s2*s3-n*s1)/(s2*s2-s4*n)             #最小二乘法获取系数的公式
a = (s3 - b*s2)/n                         #最小二乘法获取系数的公式

plt.scatter(cols1,cols2,color = 'blue')   #打印散点图
x=np.linspace(0,15,100)                   #准备x变量范围及间隔
y=b*x+a                                   #最终函数

print(a,b)    #打印结果
plt.plot(x,y,color="red")                 #打印结果曲线
plt.show()
