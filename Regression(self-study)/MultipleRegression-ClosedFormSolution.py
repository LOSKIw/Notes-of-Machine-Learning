import xlrd
import sympy as sp
import xlwt
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D 
import numpy as np
workbook=xlrd.open_workbook(r'dataset.xlsx')

sheet=workbook.sheet_by_index(0)
Y1=sheet.col_values(0)
X1=sheet.col_values(1)
X2=sheet.col_values(2)
#Axes3D
fig = plt.figure()
ax = Axes3D (fig)
ax.scatter(X1, X2, Y1)
#H为100*3矩阵，读入现有数据，第0列为1
H=[]
for i in range(100):
    values=[]
    values.append(1)
    values.append(X1[i])
    values.append(X2[i])
    H.append(values)
#将H0数组化
H0 = np.array(H) 
#H1为H的转置矩阵
H1=np.array(H0).T
H2=H1@H0
#求逆矩阵
H3=np.linalg.inv(H2)
#最终结果计算
temp=H3@H1@Y1
temp=np.mat(temp)
w0=temp[0,0]
w1=temp[0,1]
w2=temp[0,2]
#生成两坐标轴取点
x1=np.linspace(0,5000,100)
x2=np.linspace(0,5,100)
#将两坐标轴点合成
x1, x2 = np.meshgrid(x1, x2)
#结果方程，并输出最终结果图
#z=w0+w1*x1+w2*x2
ax.plot_surface(x1,x2,w0+w1*x1+w2*x2)
plt.show()
