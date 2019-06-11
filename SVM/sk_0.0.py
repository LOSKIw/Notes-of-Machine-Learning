import numpy as np
from sklearn.svm import SVC
import matplotlib.pyplot as plt

x = np.array([[3,3],[4,3],[1,1],[3,7],[1,0]])
y = np.array([1,1,-1,1,-1])
#模型
model = SVC(kernel='linear')
model.fit(x,y)
print(model.predict([[0.8, 1]]))
#绘制散点数据
a = []
b = []
for i in range(len(y)):
    if y[i]==1:
        a.append([int(x[i][0]),int(x[i][1])])
    else:
        b.append([int(x[i][0]),int(x[i][1])])
a = np.array(a)
b = np.array(b)
print(a[:,0])
plt.scatter(a[:,0],a[:,1],color = 'blue')
plt.scatter(b[:,0],b[:,1],color = 'red')
#绘制分割面

b = model.coef_[0]
w = -b[0] / b[1]
X = np.linspace(0, 5)
Y = w * X - (model.intercept_[0]) / b[1]
plt.plot(X,Y)

c = model.support_vectors_[0]
Y_down = w * X + (c[1] - w * c[0])

c = model.support_vectors_[-1]
Y_up = w * X + (c[1] - w * c[0])

plt.plot(X, Y_down, color='yellow')
plt.plot(X, Y_up, color='yellow')
#突出支持向量
plt.scatter(model.support_vectors_[:, 0],model.support_vectors_[:, 1],s=8)

plt.show()

