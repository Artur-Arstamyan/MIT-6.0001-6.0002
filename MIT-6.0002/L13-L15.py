########################################################################################################################
#                                 L13 Classification, L14 Statistical sins, L15 Wrap up
########################################################################################################################
def minkowskiDist(v1, v2, p):
    """Assumes v1 and v2 are equal-length arrays of numbers
       Returns Minkowski distance of order p between v1 and v2"""
    dist = 0.0
    for i in range(len(v1)):
        dist += abs(v1[i] - v2[i]) ** p
    return dist ** (1 / p)
  
class Passenger(object):
    # featureNames = ('C2', 'C3', 'age', 'male gender')
    # def __init__(self, pClass, age, gender, survived, name):
    #     self.name = name
    #     if pClass == 2:
    #         self.featureVec = [1, 0, age, gender]
    #     elif pClass == 3:
    #         self.featureVec = [0, 1, age, gender]
    #     else:
    #         self.featureVec = [0, 0, age, gender]
    #     self.label = survived
    #     self.cabinClass = pClass

    featureNames = ('C1', 'C2', 'C3', 'age', 'male gender')

    def __init__(self, pClass, age, gender, survived, name):
        self.name = name
        self.featureVec = [0, 0, 0, age, gender]
        self.featureVec[pClass - 1] = 1
        self.label = survived
        self.cabinClass = pClass

    def distance(self, other):
        return minkowskiDist(self.featureVec, other.featureVec, 2)

    def getClass(self):
        return self.cabinClass

    def getAge(self):
        return self.featureVec[3]

    def getGender(self):
        return self.featureVec[4]

    def getName(self):
        return self.name

    def getFeatures(self):
        return self.featureVec[:]

    def getLabel(self):
        return self.label
      
def getTitanicData(fname):
    data = {}
    data['class'], data['survived'], data['age'] = [], [], []
    data['gender'], data['name'] = [], []
    f = open(fname)
    line = f.readline()
    while line != '':
        split = line.split(',')
        data['class'].append(int(split[0]))
        data['age'].append(float(split[1]))
        if split[2] == 'M':
            data['gender'].append(1)
        else:
            data['gender'].append(0)
        if split[3] == '1':
            data['survived'].append('Survived')
        else:
            data['survived'].append('Died')
        data['name'].append(split[4:])
        line = f.readline()
    return data
  
def buildTitanicExamples(fileName):
    data = getTitanicData(fileName)
    examples = []
    for i in range(len(data['class'])):
        p = Passenger(data['class'][i], data['age'][i],
                      data['gender'][i], data['survived'][i],
                      data['name'][i])
        examples.append(p)
    print('Finished processing', len(examples), 'passengers\n')
    return examples

examples = buildTitanicExamples('TitanicPassengers.txt')

# for e in examples:
#   if e.getName()[0][-3:] == 'ian':   # or (e.getLabel() == 'Survived' and e.getFeatures()[-1] == 1):
#        print(e.getName(), e.getFeatures(), e.getLabel())

def findNearest(name, exampleSet, metric):
    for e in exampleSet:
        if e.getName() == name:
            example = e
            break
    curDist = None
    for e in exampleSet:
        if e.getName() != name:
            if curDist == None or metric(example, e) < curDist:
                nearest = e
                curDist = metric(example, nearest)
    return nearest
  
def accuracy(truePos, falsePos, trueNeg, falseNeg):
    numerator = truePos + trueNeg
    denominator = truePos + trueNeg + falsePos + falseNeg
    return numerator / denominator
  
def sensitivity(truePos, falseNeg):
    try:
        return truePos / (truePos + falseNeg)
    except ZeroDivisionError:
        return float('nan')
def specificity(trueNeg, falsePos):
    try:
        return trueNeg / (trueNeg + falsePos)
    except ZeroDivisionError:
        return float('nan')
      
def posPredVal(truePos, falsePos):
    try:
        return truePos / (truePos + falsePos)
    except ZeroDivisionError:
        return float('nan')
      
def negPredVal(trueNeg, falseNeg):
    try:
        return trueNeg / (trueNeg + falseNeg)
    except ZeroDivisionError:
        return float('nan')
      
def getStats(truePos, falsePos, trueNeg, falseNeg, toPrint=True):
    accur = accuracy(truePos, falsePos, trueNeg, falseNeg)
    sens = sensitivity(truePos, falseNeg)
    spec = specificity(trueNeg, falsePos)
    ppv = posPredVal(truePos, falsePos)
    npv = negPredVal(trueNeg, falseNeg)
    if toPrint:
        print(' Accuracy =', round(accur, 3))
        print(' Sensitivity =', round(sens, 3))
        print(' Specificity =', round(spec, 3))
        print(' Pos. Pred. Val. =', round(ppv, 3))
        print(' Neg. Pred. Val. =', round(npv, 3))
    return (accur, sens, spec, ppv, npv)
  
#                       1-st method K nearest neighbours KNN
def findKNearest(example, exampleSet, k):
    kNearest, distances = [], []
    # Build lists containing first k examples and their distances
    for i in range(k):
        kNearest.append(exampleSet[i])
        distances.append(example.distance(exampleSet[i]))
    maxDist = max(distances)  # Get maximum distance
    # Look at examples not yet considered
    for e in exampleSet[k:]:
        dist = example.distance(e)
        if dist < maxDist:
            # replace farther neighbor by this one
            maxIndex = distances.index(maxDist)
            kNearest[maxIndex] = e
            distances[maxIndex] = dist
            maxDist = max(distances)
    return kNearest, distances
  
def KNearestClassify(training, testSet, label, k):
    """Assumes training & testSet lists of examples, k an int
       Predicts whether each example in testSet has label
       Returns number of true positives, false positives,
          true negatives, and false negatives"""
    truePos, falsePos, trueNeg, falseNeg = 0, 0, 0, 0
    for testCase in testSet:
        nearest, distances = findKNearest(testCase, training, k)
        # conduct vote
        numMatch = 0
        for ex in nearest:
            if ex.getLabel() == label:
                numMatch += 1
        if numMatch > k // 2:  # guess label
            if testCase.getLabel() == label:
                truePos += 1
            else:
                falsePos += 1
        else:  # guess not label
            if testCase.getLabel() != label:
                trueNeg += 1
            else:
                falseNeg += 1
    return truePos, falsePos, trueNeg, falseNeg
  
knn = lambda training, testSet: KNearestClassify(training, testSet, 'Survived', 3)
#                       2-nd method Logistic regression
def buildModel(examples, toPrint=True):
    featureVecs, labels = [], []
    for e in examples:
        featureVecs.append(e.getFeatures())
        labels.append(e.getLabel())
    LogisticRegression = sklearn.linear_model.LogisticRegression
    model = LogisticRegression().fit(featureVecs, labels)
    if toPrint:
        print('model.classes_ =', model.classes_)
        print(model.coef_, model.coef_[0])
        for i in range(len(model.coef_)):
            print('For label', model.classes_[1])
            for j in range(len(model.coef_[0])):
                print('   ', Passenger.featureNames[j], '=', model.coef_[i][j])
    return model
  
def applyModel(model, testSet, label, prob=0.5):
    testFeatureVecs = [e.getFeatures() for e in testSet]
    probs = model.predict_proba(testFeatureVecs)
    truePos, falsePos, trueNeg, falseNeg = 0, 0, 0, 0
    for i in range(len(probs)):
        if probs[i][1] > prob:
            if testSet[i].getLabel() == label:
                truePos += 1
            else:
                falsePos += 1
        else:
            if testSet[i].getLabel() != label:
                trueNeg += 1
            else:
                # print(testSet[i].getName(), testSet[i].getFeatures())
                falseNeg += 1
    return truePos, falsePos, trueNeg, falseNeg
  
def lr(trainingData, testData, prob=0.5):
    model = buildModel(trainingData, False)
    results = applyModel(model, testData, 'Survived', prob)
    return results
  
#                       LOO & split 80-20  testing methods
def leaveOneOut(examples, method, toPrint=True):
    truePos, falsePos, trueNeg, falseNeg = 0, 0, 0, 0
    for i in range(len(examples)):
        testCase = examples[i]
        trainingData = examples[0:i] + examples[i + 1:]
        results = method(trainingData, [testCase])
        truePos += results[0]
        falsePos += results[1]
        trueNeg += results[2]
        falseNeg += results[3]
    if toPrint:
        getStats(truePos, falsePos, trueNeg, falseNeg)
    return truePos, falsePos, trueNeg, falseNeg
  
def split80_20(examples):
    sampleIndices = random.sample(range(len(examples)), len(examples) // 5)
    trainingSet, testSet = [], []
    for i in range(len(examples)):
        if i in sampleIndices:
            testSet.append(examples[i])
        else:
            trainingSet.append(examples[i])
    return trainingSet, testSet
  
def randomSplits(examples, method, numSplits, toPrint=True):
    truePos, falsePos, trueNeg, falseNeg = 0, 0, 0, 0
    random.seed(0)
    for t in range(numSplits):
        trainingSet, testSet = split80_20(examples)
        results = method(trainingSet, testSet)
        truePos += results[0]
        falsePos += results[1]
        trueNeg += results[2]
        falseNeg += results[3]
    getStats(truePos, falsePos, trueNeg, falseNeg, toPrint)
    return truePos / numSplits, falsePos / numSplits, trueNeg / numSplits, falseNeg / numSplits
  
#                       ROC  -  Receiver operating characteristics
def buildROC(trainingSet, testSet, title, plot=True):
    model = buildModel(trainingSet, True)
    xVals, yVals = [], []
    p = 0.0
    while p <= 1.0:
        truePos, falsePos, trueNeg, falseNeg = applyModel(model, testSet, 'Survived', p)
        xVals.append(1.0 - specificity(trueNeg, falsePos))
        yVals.append(sensitivity(truePos, falseNeg))
        p += 0.01
    auroc = sklearn.metrics.auc(xVals, yVals)
    if plot:
        plt.plot(xVals, yVals)
        plt.plot([0, 1], [0, 1])
        title = title + '\nAUROC = ' + str(round(auroc, 3))
        plt.title(title)
        plt.xlabel('1 - specificity')
        plt.ylabel('Sensitivity')
        plt.show()
    return auroc


numSplits = 10
print('Average of', numSplits, '80/20 splits using KNN (k=3)')
truePos, falsePos, trueNeg, falseNeg = randomSplits(examples, knn, numSplits)
print('Average of LOO testing using KNN (k=3)')
truePos, falsePos, trueNeg, falseNeg = leaveOneOut(examples, knn)

random.seed(0)
numSplits = 10
print('Average of', numSplits, '80/20 splits LR')
truePos, falsePos, trueNeg, falseNeg = randomSplits(examples, lr, numSplits)
print('Average of LOO testing using LR')
truePos, falsePos, trueNeg, falseNeg = leaveOneOut(examples, lr)

# Look at weights
trainingSet, testSet = split80_20(examples)
model = buildModel(trainingSet, True)

#   Look at changing prob
random.seed(0)
trainingSet, testSet = split80_20(examples)
model = buildModel(trainingSet, False)
for p in [0.1, 0.9]:
    print('Try p =', p)
    truePos, falsePos, trueNeg, falseNeg = applyModel(model, testSet, 'Survived', p)
    print(truePos, falsePos, trueNeg, falseNeg)
    getStats(truePos, falsePos, trueNeg, falseNeg)
    
random.seed(0)
trainingSet, testSet = split80_20(examples)
print(buildROC(trainingSet, testSet, 'ROC for Predicting Survival, 1 Split'))
