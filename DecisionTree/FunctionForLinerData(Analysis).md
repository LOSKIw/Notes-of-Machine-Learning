由于上一例的实现中只针对了离散数据，为了扩充处理范围，我实现了一下对线性数据的简单处理，在其中我选择用中位数作为指标，平均数、众数等等其他数据在我看来异曲同工，最终也都会有较相似的结构。  

- **求连续数据的香农熵**  
```
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
```  
与离散数据的处理极其相似，不过在我看来使用上并不会太多，毕竟我们在分类的时候一般不会还是在用如此繁琐连续的数据进行比对。  
简单来说，就是建立一个字典，把通过指标分类的数据分别计数(在这里是大于等于指标一类，剩余为另一类)，最后再使用计算香农熵的方法正常计算，变化并不大，只是有了中间一步分类的过度。  

- **求连续数据指标：中位数**  
```
def getLinerFlag(dataSet,axis):
    num=len(dataSet)
    for i in range(num):
        feature = [ example[axis] for example in dataSet]
        feature2 = sorted( feature )
    flag = feature[int(num/2)]
    return flag
```  
这个函数并不重要启示，毕竟实际上有更多更好的衡量分类指标，这里只是一个简单和偷懒的衡量方法。其他方法在我看来整体结构上应该类似，可能只是公式不同。  
  

- **线性划分**  
```
def splitDataSet(dataset, axis, value):
    retDataSet = []
    for featVec in dataset:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
```  
依旧有着相似的性质，主要取决于采取的衡量方法，我觉得连续数据的划分方法比较不同的可能就是指标选取的数目，这里只有一个，所以较轻松。如果有多个，可以从低到高依次抽取，并删除选取过的，当然或许有更多的，需要完全不同方式的衡量方式，我目前还没有考虑到。  
  
- **加入判断连续以及离散数据的最优划分求解**  
```
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
```  
毕竟离散数据连续数据混用应该是常态，这里我索性就综合的进行了架构。其中我对于连续以及离散的判断非常简单，就是一个属性的分类如果超过了5个，就判定为线性(或者说还得是数字?)，可能不是那么的科学，不过...先这样吧。  
```
f=getLinerFlag(dataSet,i)
            datah,datal=LinerSplit(dataSet,i,f)
            newEntropy = len(datal)/float(len(dataSet))*calcShannonEnt(datah)+\
            len(datah)/float(len(dataSet))*calcShannonEnt(datal)
```  
理解起来应该也非常通俗易懂，先求得大于等于以及小于划分指标的两个集合，之后计算此划分的香农熵，就可以正常比对了。
