2019/4/7
许久未有更新，大概有清明的缘故，但是主要是决策树的实现太...繁琐了。
如果只是接受他的原理的话还好说，但是要想用代码去实现比较糟心，目前运用了《机器学习实战》的代码手打了一遍，决定在这里一点点摸索一下该工程。
实例的代码在使用上运用了香农熵，并且都是来处理离散数据的，因此有一些局限性，但是对其进行深层次的解析有利于对于代码的运作，python语言的特点及书写肯定是有帮助的。
我们分别从每个函数开始：

- **计算香农熵**  

```
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
```
该函数为当前的数据集计算香农熵。
其中，numEntries用来计数数据数目
`numEntries = len(dataSet)`
其后，该函数运用了一个字典来计算各个**最终类**(即我们所要最终分开的特点的所有类型，比如Titanic题目中就是是否生还,Coursera课程中的例子就是这个贷款是否安全)的出现数目，其中，该最终数据是处在数据集的最后一列的，因此运用
`currentLabel = featVec[-1]`
让currentLabel暂时记住当前数据的最终类型，倘使该类型不存在，就要用
```
 if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
```
将其插入字典并将它的键值初始化为0(即出现0次)，最后用
`labelCounts[currentLabel] +=1`
计数代表当前最终类型出现数目+1
之后便是对于香农熵的计算，这里的代码上的理解并不困难
```
for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)
```
log(prob,2)是以2为底数求对数  

- **划分数据集**  
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
该函数使用了三个参数：待划分的数据集，划分数据集的特征(即第axis个属性)，需要返回的特征的值(该属性的取值value)。  
首先由于需要将一类数据放于一起，但是python在函数中传递的是列表的引用，直接修改也会在全局上对列表产生变化，为了避免这种影响就需要新建一个空表存储目标数据。  
`retDataSet = []`  
再之后就是要将相应的数据放入这个列表中。  
其中为了更好的进行以下的操作，因为本工程控制划分数目的方式看来是限定在一条线路中每个属性最多有一次作为划分指标，因此需要将其在加入retDataSet时去除，由下列代码实现：
```
reducedFeatVec = featVec[:axis]
reducedFeatVec.extend(featVec[axis+1:])
retDataSet.append(reducedFeatVec)
```  
书中提到了append()与extend()函数的区别，前者可以将列表整体作为一个元素加入新列表，后者则是将列表的元素分别加入新列表。  

- **选出最好的划分方式**  
  
```
def chooseBestFeatureToSplit(dataset):
    numFeatures = len(dataset[0]) - 1
    baseEntropy = calcShannonEnt(dataset)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataset]
        uniqueVals=set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataset,i,value)
            prob = len(subDataSet)/float(len(dataset))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain>bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature
```  
当下我们所要做的是要遍历当前的数据集，不断计算所有属性划分对应的香农熵，由此选出最适合作为当前状况下划分标准的属性。  
为了防止最终属性被选择，我们需要将其排除在外，默认最终属性一般会出现在最后一列，  
`numFeatures = len(dataset[0]) - 1`  
之后在for循环中numFeatures数目便不会再囊括最终属性了。  
在这个时候我纠结了一下，万一最好的划分就是最终属性呢？不过目前我已经说服自己了，毕竟最终属性是我们的目标，不管怎样我们都要避开它并使用别的属性来进行划分。  
之后初始化变量，分别来存储新的香农熵变化和当前数据。  
```
bestInfoGain = 0.0
bestFeature = -1
```  
现在进入这个遍历所有属性的for大循环。一开始我们先将当前属性的所有可能值传入一个空集合(即无重复元素的集合)。  
```
featList = [example[i] for example in dataset]
uniqueVals=set(featList)
```  
而下面这个变量来计算当前香农熵。  
```
newEntropy = 0.0
for value in uniqueVals:
            subDataSet = splitDataSet(dataset,i,value)
            prob = len(subDataSet)/float(len(dataset))
            newEntropy += prob * calcShannonEnt(subDataSet)
infoGain = baseEntropy - newEntropy
```  
其中用splitDataSet()，将当前处理的属性作为划分依据，用其内部所有可能的取值来分出子集，并计算对应的香农熵，然后根据比例再加权求和，得到该属性划分下的香农熵newEntropy以及相比直接作为叶子节点得到的香农熵的差infoGain。  
```
if(infoGain>bestInfoGain):
        bestInfoGain = infoGain
        bestFeature = i
```  
最后与当前记录的最优属性的结果比对，如果更好就覆盖。最后返回最优属性。  

- **选取出现最多的属性**  
  
```
def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():classCount[vote]=0
        classCount[vote] += 1
    sortedClassCount = sorted(classClount.iteritems(),\
                              key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
```  
如果当前划分时已经没有更多的属性了，那么该节点自动变为叶子节点，其分类由其数据中最终属性出现最多的分类决定，即根据属性的分类创建一个字典classCount，并用分类作为键，出现次数为对应值。  
随后用operator库中的sort()函数为其排序，选出出现最多的最终属性，以此作为该叶子节点的分类。  
  
  
- **主体：创建树**  
```
def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0])==1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree
```  
这个函数运用了递归的想法，最终结果是以字典中的字典形式来表示的，虽然并不是特别直观，但至少是我能接受的工程量。  
首先进行了两个判断，一是若当前数据集在最终分类上已经达成了共识，那么就不需要在进行分类了：  
```
if classList.count(classList[0]) == len(classList):
        return classList[0]
```  
二，如果所有的属性已经被使用(排除，仅剩最终属性)，也会停止递归：  
```
if len(dataSet[0])==1:
        return majorityCnt(classList)
```  
在排除了以上情况后就会选择出当前最优的划分属性，并在其中开辟对应的子字典：
```
bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{ } }
```  
并删除已经使用的属性：  
`del(labels[bestFeat])`  
紧接着要为上面刚选定的属性分类划分出各个子节点，并为其递归再次生成子树，方法集合了上文的许多技巧，暂时不再赘述。

以上，是我对于《机器学习实战》中的决策树实现代码的解析。
