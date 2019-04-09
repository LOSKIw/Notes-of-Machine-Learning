from math import log
import operator

#对连续数据的香农熵求值：使用中位数作为flag
def calcLinerData(dataSet):
    num=len(dataSet)
    count={1:0,0:0}
    shannonEnt=0.0
    for i in range(num):
        feature = [ example[-1] for example in dataSet]
        feature2 = sorted( feature )
    flag = feature[int(num/2)]
    for i in range(num):
        if feature[i]>= flag:
            feature[i]=1
            count[1]+=1
        else:
            feature[i]=0
            count[0]+=1
    for i in [0,1]:
        prob = float(count[i])/num
        shannonEnt -= prob * log(prob,2)
    return shannonEnt
#离散求解香农熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] +=1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt
#线性求中位数
def getLinerFlag(dataSet,axis):
    num=len(dataSet)
    count={1:0,0:0}
    shannonEnt=0.0
    for i in range(num):
        feature = [ example[axis] for example in dataSet]
        feature2 = sorted( feature )
    flag = feature[int(num/2)]
    return flag

#线性划分
def LinerSplit(dataSet,axis,value):
    Datahigh=[]
    Datalow=[]
    for featVec in dataSet:
        if featVec[axis]>=value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            Datahigh.append(reducedFeatVec)
        else:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            Datalow.append(reducedFeatVec)
    return Datahigh,Datalow
#离散划分
def splitDataSet(dataset, axis, value):
    retDataSet = []
    for featVec in dataset:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
#加入线性判断的最优属性选取
def chooseLinerSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals=set(featList)
        newEntropy = 0.0
        if len(uniqueVals)>5:
            f=getLinerFlag(dataSet,i)
            datah,datal=LinerSplit(dataSet,i,f)
            newEntropy = len(datal)/float(len(dataSet))*calcShannonEnt(datah)+\
            len(datah)/float(len(dataSet))*calcShannonEnt(datal)
        else:
            for value in uniqueVals:
                subDataSet = splitDataSet(dataSet,i,value)
                prob = len(subDataSet)/float(len(dataSet))
                newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain>bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


data=[[2,10,1],[10,2,0],[10,7,1],[2,4,1],[2,5,0],[4,7,1]]
print(chooseLinerSplit(data))
