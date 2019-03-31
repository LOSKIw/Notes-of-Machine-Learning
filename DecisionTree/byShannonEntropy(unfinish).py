from math import log
import csv
import numpy as np

#求整个数据集的信息熵，其中，currentLabel按行读入最终结果的那一部分数据，并为不
#同的结果分别计数，最后计算香农熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[4]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] +=1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

label=['num','HP','name','sex','age','sibsp','parch','ticket','fare','cabin','embarked']
datacsv = csv.reader(open("train.csv"))

data=[]
for line in datacsv:
    data.append(line)
data=np.array(data)
print(type(data))
print(data)
a=calcShannonEnt(data)
print(a)
