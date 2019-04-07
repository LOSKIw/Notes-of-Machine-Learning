2019/4/7
许久未有更新，大概有清明的缘故，但是主要是决策树的实现太...繁琐了。
如果只是接受他的原理的话还好说，但是要想用代码去实现比较糟心，目前运用了《机器学习实战》的代码手打了一遍，决定在这里一点点摸索一下该工程。
实例的代码在使用上运用了香农熵，并且都是来处理离散数据的，因此有一些局限性，但是对其进行深层次的解析有利于对于代码的运作，python语言的特点及书写肯定是有帮助的。
我们分别从每个函数开始：

1. 计算香农熵

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
其中log(prob,2)是以2为底数求对数
