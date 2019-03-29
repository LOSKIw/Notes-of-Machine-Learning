import xlrd
import xlwt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import numpy as np

workbook=xlrd.open_workbook(r'dataset.xlsx')

sheet=workbook.sheet_by_index(0)
Y1=sheet.col_values(0)
X1=sheet.col_values(1)
X2=sheet.col_values(2)
#将训练数据的散点图打印出来
fig = plt.figure()
ax = Axes3D (fig)
ax.scatter(X1, X2, Y1)

#将X1，X2的元素及一列1组合为一个矩阵
H=[]
for i in range(100):
    values=[]
    values.append(1)
    values.append(X1[i])
    values.append(X2[i])
    H.append(values)
#根据公式，准备变量
#把H从list类型转化为数组
H0 = np.mat(H)
#H的转置
H1=np.mat(H0).T


H2=H1@H0


H3=np.linalg.inv(H2)
print(H3)
print(H0)

temp=H3@H1@Y1

temp=np.mat(temp)
print(type(temp))
print(temp)
w0=temp[0,0]
w1=temp[0,1]
w2=temp[0,2]

x1=np.linspace(0,5000,1)
x2=np.linspace(0,10,1)
#x1,x2=np.meshgrid(x1,x2)

fig2=plt.figure()
ax2 = Axes3D (fig2)
print(w0,w1,w2)

def func(x,y):
    return w0+w1*x+w2*y

z=func(x1,x2)
for i in range(100):
    print(func(X1[i],X2[i])-Y1[i])
plt.show()
