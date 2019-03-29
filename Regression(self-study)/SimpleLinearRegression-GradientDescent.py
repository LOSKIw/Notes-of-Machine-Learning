import xlrd
import xlwt
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
workbook=xlrd.open_workbook(r'1.xls')

sheet=workbook.sheet_by_index(0)
cols1=sheet.col_values(0)                           #获取第一列
cols2=sheet.col_values(1)                           #获取第二列

#a+b
#a=sp.Symbol('a')
#b=sp.Symbol('b')
#已知结果约为a=-22.63450339669057 b=13.449314363947979
#求方差
def get_sqm(a,b):
    sqm=0
    for i in range(100):
        sqm=sqm+(cols2[i]-a-b*cols1[i])*(cols2[i]-a-b*cols1[i])
    return sqm
#分别准备对a,b求偏导的函数
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
#n为逼近时的系数，非常重要
n=0.0001
#初始化a,b两值
a=0.0
b=0.0
while abs(get_pa(a,b))>=1 and abs(get_pb(a,b))>=1 :
    c=a
    d=b
    a=a-n*get_pa(c,d)
    b=b-n*get_pb(c,d)
    print(get_sqm(a,b))
#输出结果
print(a,b)
#绘制散点图
plt.scatter(cols1,cols2,color = 'blue')
#绘制结果图
x=np.linspace(0,15,100)
y=b*x+a
plt.plot(x,y,color="red")
plt.show()
