import time
import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import pandas as pd
import sklearn.linear_model

########################################################################################################################
#                    6.0002 MIT COURSE INTRODUCTION TO COMPUTATIONAL THINKING AND DATA SCIENCE
########################################################################################################################
########################################################################################################################
#                                 L13 Classification, L14 Statistical sins, L15 Wrap up
########################################################################################################################

a = np.array([5, 6, 7])
print(a)
'''
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
'''
########################################################################################################################
#                                              L12 Clustering
########################################################################################################################
'''
class Patient(utils.Example):
    pass


def scaleAttrs(vals):
    vals = np.array(vals)
    mean = sum(vals) / len(vals)
    sd = np.std(vals)
    vals = vals - mean
    return vals / sd


def getData(toScale=False):
    # read in data
    hrList, stElevList, ageList, prevACSList, classList = [], [], [], [], []
    cardiacData = open('cardiacData.txt', 'r')
    for l in cardiacData:
        l = l.split(',')
        hrList.append(int(l[0]))
        stElevList.append(int(l[1]))
        ageList.append(int(l[2]))
        prevACSList.append(int(l[3]))
        classList.append(int(l[4]))
    if toScale:
        hrList = scaleAttrs(hrList)
        stElevList = scaleAttrs(stElevList)
        ageList = scaleAttrs(ageList)
        prevACSList = scaleAttrs(prevACSList)
    # Build points
    points = []
    for i in range(len(hrList)):
        features = np.array([hrList[i], prevACSList[i], stElevList[i], ageList[i]])
        pIndex = str(i)
        points.append(Patient('P' + pIndex, features, classList[i]))
    return points


def kmeans(examples, k, verbose=False):
    # Get k randomly chosen initial centroids, create cluster for each
    initialCentroids = random.sample(examples, k)
    clusters = []
    for e in initialCentroids:
        clusters.append(utils.Cluster([e]))

    # Iterate until centroids do not change
    converged = False
    numIterations = 0
    while not converged:
        numIterations += 1
        # Create a list containing k distinct empty lists
        newClusters = []
        for i in range(k):
            newClusters.append([])

        # Associate each example with closest centroid
        for e in examples:
            # Find the centroid closest to e
            smallestDistance = e.distance(clusters[0].getCentroid())
            index = 0
            for i in range(1, k):
                distance = e.distance(clusters[i].getCentroid())
                if distance < smallestDistance:
                    smallestDistance = distance
                    index = i
            # Add e to the list of examples for appropriate cluster
            newClusters[index].append(e)

        for c in newClusters:  # Avoid having empty clusters
            if len(c) == 0:
                raise ValueError('Empty Cluster')

        # Update each cluster; check if a centroid has changed
        converged = True
        for i in range(k):
            if clusters[i].update(newClusters[i]) > 0.0:
                converged = False
        if verbose:
            print('Iteration #' + str(numIterations))
            for c in clusters:
                print(c)
            print('')  # add blank line
    return clusters


def trykmeans(examples, numClusters, numTrials, verbose=False):
    """Calls kmeans numTrials times and returns the result with the
          lowest dissimilarity"""
    best = kmeans(examples, numClusters, verbose)
    minDissimilarity = utils.dissimilarity(best)
    trial = 1
    while trial < numTrials:
        try:
            clusters = kmeans(examples, numClusters, verbose)
        except ValueError:
            continue  # If failed, try again
        currDissimilarity = utils.dissimilarity(clusters)
        if currDissimilarity < minDissimilarity:
            best = clusters
            minDissimilarity = currDissimilarity
        trial += 1
    return best


def printClustering(clustering):
    """Assumes: clustering is a sequence of clusters
       Prints information about each cluster
       Returns list of fraction of pos cases in each cluster"""
    posFracs = []
    for c in clustering:
        numPts = 0
        numPos = 0
        for p in c.members():
            numPts += 1
            if p.getLabel() == 1:
                numPos += 1
        fracPos = numPos / numPts
        posFracs.append(fracPos)
        print(c, '\nCluster of size', numPts, 'with fraction of positives =', round(fracPos, 4))
    return np.array(posFracs)


def testClustering(patients, numClusters, seed=0, numTrials=5):
    random.seed(seed)
    bestClustering = trykmeans(patients, numClusters, numTrials)
    posFracs = printClustering(bestClustering)
    return posFracs


patients = getData(True)
for k in (2, 4):
    print('\n     Test k-means (k = ' + str(k) + ')')
    posFracs = testClustering(patients, k, 2)

numPos = 0
for p in patients:
    if p.getLabel() == 1:
        numPos += 1
print('Total number of positive patients =', numPos)

'''
########################################################################################################################
#                                              L11 Intro to Machine Learning
########################################################################################################################
'''
def variance(X):
    mean = float(sum(X)) / len(X)
    diffs = 0.0
    for x in X:
        diffs += (x - mean) ** 2
    return diffs / len(X)
def stdDev(X):
    return variance(X) ** 0.5
def minkowskiDist(v1, v2, p):
    """Assumes v1 and v2 are equal-length arrays of numbers
       Returns Minkowski distance of order p between v1 and v2"""
    dist = 0.0
    for i in range(len(v1)):
        dist += abs(v1[i] - v2[i]) ** p
    return dist ** (1.0 / p)
class Animal(object):
    def __init__(self, name, features):
        """Assumes name a string; features a list of numbers"""
        self.name = name
        self.features = np.array(features)

    def getName(self):
        return self.name

    def getFeatures(self):
        return self.features

    def distance(self, other):
        """Assumes other an Animal
           Returns the Euclidean distance between feature vectors
              of self and other"""
        return minkowskiDist(self.getFeatures(), other.getFeatures(), 2)
def compareAnimals(animals, precision):
    """Assumes animals is a list of animals, precision an int >= 0
       Builds a table of Euclidean distance between each animal"""
    # Get labels for columns and rows
    columnLabels = []
    for a in animals:
        columnLabels.append(a.getName())
    rowLabels = columnLabels
    tableVals = []
    # Get distances between pairs of animals
    # For each row
    for a1 in animals:
        row = []
        # For each column
        for a2 in animals:
            if a1 == a2:
                row.append('--')
            else:
                distance = a1.distance(a2)
                row.append(str(round(distance, precision)))
        tableVals.append(row)
    # Produce table
    table = plt.table(rowLabels=rowLabels, colLabels=columnLabels, cellText=tableVals, cellLoc='center', loc='center',
                      colWidths=[0.2] * len(animals))
    table.scale(1, 3)
    plt.title('Eucliedan Distance Between Animals')
    plt.show()

#  Actual number of legs
cobra = Animal('cobra', [1, 1, 1, 1, 0])
rattlesnake = Animal('rattlesnake', [1, 1, 1, 1, 0])
boa = Animal('boa\nconstrictor', [0, 1, 0, 1, 0])
chicken = Animal('chicken', [1, 1, 0, 1, 2])
alligator = Animal('alligator', [1, 1, 0, 1, 4])
dartFrog = Animal('dart frog', [1, 0, 1, 0, 4])
zebra = Animal('zebra', [0, 0, 0, 0, 4])
python = Animal('python', [1, 1, 0, 1, 0])
guppy = Animal('guppy', [0, 1, 0, 0, 0])
animals = [cobra, rattlesnake, boa, chicken, guppy, dartFrog, zebra, python, alligator]
compareAnimals(animals, 3)
'''
########################################################################################################################
#           ||||||||||||||||||                   MatPlotLib                          |||||||||||||||||||||
########################################################################################################################
#                                                Basic  Graph
'''
plt.figure(figsize=(5, 4), dpi=100)
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.title("Functions", fontname='Comic Sans MS', size=25)  # fontdict={'fontname': 'Comic Sans MS', 'fontsize': 20}

x1 = np.arange(0, 5, 0.5)

plt.plot([0, 1, 2, 3, 4, 5], [14, 25, 1, 3, 4, 19], 'co--', label="sin", linewidth='2',
         markerfacecolor='b', markeredgecolor='r', markersize='6')
plt.plot(x1[:6], x1[:6] ** 2, 'g^-', label="f(x)=x^2", markerfacecolor='m', markersize='10', markeredgecolor='k')
plt.plot(x1[5:], x1[5:] ** 2, 'r^--', label="f(x)=x^2", markerfacecolor='m', markersize='10', markeredgecolor='k')
# plt.xticks([1, 3, 5, 25])
# plt.yticks([1, 3, 5, 25])
plt.legend()
# plt.xlim(1, 3)
# plt.ylim(1, 50)
plt.savefig('myGraph.png', dpi=300)
plt.show()
'''
#                                                   Bar Chart
'''
labels = ['A', 'B', 'C']
values = [1, 4, 2]

plt.figure(figsize=(5, 3), dpi=100)
bars = plt.bar(labels, values)
patterns = ['/', 'O', '*']
for bar in bars:
    bar.set_hatch(patterns.pop(0))

plt.savefig('barchart.png', dpi=300)
plt.show()
'''
#                                                  Line Graph
'''
gas = pd.read_csv('gas_prices.csv')
plt.figure(figsize=(8, 5))
plt.title('Gas Prices over Time (in USD)', fontdict={'fontweight': 'bold', 'fontsize': 18})
plt.plot(gas.Year, gas.USA, 'b.-', label='United States')
plt.plot(gas.Year, gas.Canada, 'r.-')
plt.plot(gas.Year, gas['South Korea'], 'g.-')
plt.plot(gas.Year, gas.Australia, 'y.-')

# Another Way to plot many values!
# countries_to_look_at = ['Australia', 'USA', 'Canada', 'South Korea']
# for country in gas:
#     if country in countries_to_look_at:
#         plt.plot(gas.Year, gas[country], marker='.')

plt.xticks(gas.Year[::3].tolist()+[2011])
plt.xlabel('Year')
plt.ylabel('US Dollars')

plt.legend()
plt.savefig('Gas_price_figure.png', dpi=300)
plt.show()
'''
#                                            Fifa data HISTOGRAM
'''
fifa = pd.read_csv('fifa_data.csv')
fifa.head(5)
bins = [40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
plt.figure(figsize=(8, 5))
plt.hist(fifa.Overall, bins=bins, color='#abcdef')
plt.xticks(bins)
plt.ylabel('Number of Players')
plt.xlabel('Skill Level')
plt.title('Distribution of Player Skills in FIFA 2018')
plt.savefig('histogram.png', dpi=300)
plt.show()
'''

#                                                    Fifa data PIE
'''
fifa = pd.read_csv('fifa_data.csv')
left = fifa.loc[fifa['Preferred Foot'] == 'Left'].count()[0]
right = fifa.loc[fifa['Preferred Foot'] == 'Right'].count()[0]
plt.figure(figsize=(8, 5))
labels = ['Left', 'Right']
colors = ['#abcdef', '#aabbcc']
plt.pie([left, right], labels=labels, colors=colors, autopct='%.2f %%')
plt.title('Foot Preference of FIFA Players')
plt.show()
'''
#                                            Fifa data PIE-2 weights
'''
fifa = pd.read_csv('fifa_data.csv')
plt.figure(figsize=(8, 5), dpi=100)
# plt.style.use('ggplot')

fifa.Weight = [int(x.strip('lbs')) if type(x) == str else x for x in fifa.Weight]

light = fifa.loc[fifa.Weight < 125].count()[0]
light_medium = fifa[(fifa.Weight >= 125) & (fifa.Weight < 150)].count()[0]
medium = fifa[(fifa.Weight >= 150) & (fifa.Weight < 175)].count()[0]
medium_heavy = fifa[(fifa.Weight >= 175) & (fifa.Weight < 200)].count()[0]
heavy = fifa[fifa.Weight >= 200].count()[0]

weights = [light, light_medium, medium, medium_heavy, heavy]
label = ['under 125', '125-150', '150-175', '175-200', 'over 200']
explode = (.5, .2, 0, 0, .5)
plt.title('Weight of Professional Soccer Players (lbs)')
plt.pie(weights, labels=label, colors=['r', 'b', '#ccbbcc', 'g', 'k'], explode=explode,
        pctdistance=0.8, autopct='%.2f %%')
plt.show()
'''
#                                          Box and Whiskers Chart
'''
fifa = pd.read_csv('fifa_data.csv')
plt.figure(figsize=(5, 8), dpi=100)
plt.style.use('default')
print(fifa.groupby('Club').mean().sort_values('Overall', ascending=False))
barcelona = fifa.loc[fifa.Club == "FC Barcelona"]['Overall']
madrid = fifa.loc[fifa.Club == "Real Madrid"]['Overall']
revs = fifa.loc[fifa.Club == "New England Revolution"]['Overall']

# bp = plt.boxplot([barcelona, madrid, revs], labels=['a','b','c'], boxprops=dict(facecolor='red'))
bp = plt.boxplot([barcelona, madrid, revs], labels=['FC Barcelona', 'Real Madrid', 'NE Revolution'], patch_artist=True,
                 medianprops={'linewidth': 2})

plt.title('Professional Soccer Team Comparison')
plt.ylabel('FIFA Overall Rating')

for box in bp['boxes']:
    # change outline color
    box.set(color='#4286f4', linewidth=2)
    # change fill color
    box.set(facecolor='#e0e0e0')
    # change hatch
    # box.set(hatch = '/')

plt.show()
'''
'''
plt.xlabel("Numbers 0-99")
plt.ylabel("Percentage of appearances")
plt.title("1000 random positive numbers range(0,100)", fontname='Comic Sans MS', size=10)
x2 = np.arange(0, 100, 1)
y2 = [[random.randint(0, 99) for i in range(1000)].count(n)/10 for n in range(100)]
plt.plot(x2, y2, 'ok', linestyle="None")
plt.show()
'''
########################################################################################################################
#        ||||||||||||                  Experimenting  POKEMON  data  with pandas              |||||||||||||||
########################################################################################################################
'''
print(df.columns)f_xlsx = pd.read_csv('pokemon_data.txt', delimiter="\t")
# df_xlsx = pd.read_excel('pokemon_data.xlsx')
# df = pd.read_csv('pokemon_data.csv')
print(df[['Generation', 'Name']], df['Speed'])
print(df.iloc[750:1000])
print(df.iloc[list(range(1, 4)) + [7, 8, 11]])
print(df.iloc[4, 1])
for index, row in df.iterrows():
    print(index, row['Name'])
print(df[['Generation', 'Name']], df.loc[df['Type 1'] == 'Fire'], sep="\n")
print(df.iloc[[1, 4, 6, 799], [1, 2, 9]], 
      df.loc[[1, 4, 6, 799], ['Name', 'Type 1', 'Speed']], sep='\n')
for i in df['Name']:                   
    print(i)

print(df.describe())
print(df.loc[[429, 428, 154, 71], ['Name', 'Speed', 'Attack']])
df = df.sort_values(['Speed', 'Attack'], ascending=[0, 1])
print(df.sort_index())

df = df.sort_values('Total', ascending=False)
print(df)
print(df.loc[[0, 426]])
print(df.iloc[[0, 426]])   # you can see difference between loc and iloc here    df.iloc[raw index]    df.loc[raw label]
df.reset_index(drop=True, inplace=True)  # or df = df.reset_index(drop=True)   

df['Total'] = df['HP'] + df['Attack'] + df['Defense'] + df['Sp. Atk'] + df['Sp. Def'] + df['Speed']
df = df.drop(columns=['Total'])
df['Total'] = df.iloc[:, 4:10].sum(axis=1)
cols = list(df.columns.values)
df = df[cols[:4] + cols[-1:] + cols[4:-1]]
# df.to_csv('modified.csv',  index=False)
# df.to_csv('modified.txt',  index=False, sep='\t')
# df.to_excel('modified.xlsx', index=False)

df = pd.read_csv('modified.csv')
print(df.loc[~df['Name'].str.contains('Mega')])
print(df.loc[df['Type 1'].str.contains('fire|grass', flags=re.I, regex=True)])
print(df.loc[df['Name'].str.contains('^pi[a-z]*', flags=re.I, regex=True)])
df.loc[df['Type 1'] == 'Fire', 'Type 1'] = 'Flamer'
print(df)
df.loc[df['Total'] >= 600, ['Generation', 'Legendary']] = [10, "Go fuck yourself"]
print(df.iloc[450:500, [1, 4, -2, -1]])

df = pd.read_csv('modified.csv')
print(df.groupby(['Type 1']).mean().sort_values('Attack', ascending=False))  # sum() count()
df['Count'] = 1
print(df.groupby(['Type 1', 'Type 2']).count()['Count'])
new_df = pd.DataFrame(columns=df.columns)
for df in pd.read_csv('modified.csv', chunksize=5):
    result = df.groupby(['Type 1']).count()
    new_df = pd.concat([new_df, result])
df = pd.read_csv('modified.csv')
new = df.iloc[:, 3:-1]
print(pd.concat([new, df], ignore_index=True))
'''
########################################################################################################################
#                                        L10 UNDERSTANDING EXPERIMENTAL DATA
########################################################################################################################
########################################################################################################################
#                                        L9 UNDERSTANDING EXPERIMENTAL DATA
########################################################################################################################
# my own polyfit
'''
def sqr(a, b, x, y):
    s = 0
    for i in range(len(x)):
        s += (a*x[i]+b-y[i])**2
    return s
def lr(x, y):
    a = 1000
    b = 1000
    min = sqr(a, b, x, y)
    for i in range(-1000, 1000):
        for j in range(-1000, 1000):
            if min > sqr(i, j, x, y):
                min = sqr(i, j, x, y)
                a = i
                b = j
    return a, b
'''
'''
def getData(fileName):
    dataFile = open(fileName, 'r')
    distances = []
    masses = []
    dataFile.readline()  # discard header
    for line in dataFile:
        d, m = line.split()
        distances.append(float(d))
        masses.append(float(m))
    dataFile.close()
    return (masses, distances)
def labelPlot():
    plt.title('Measured Displacement of Spring')
    plt.xlabel('|Force| (Newtons)')
    plt.ylabel('Distance (meters)')
def plotData(fileName):
    m, d = getData(fileName)
    m = np.array(m)
    d = np.array(d)
    f = m * 9.81  # get force
    plt.plot(f, d, 'bo', label='Measured points')
    labelPlot()
def fitData(fileName):
    m, d = getData(fileName)
    m = np.array(m)
    d = np.array(d)
    f = m * 9.81  # get force
    plt.plot(f, d, 'bo', label='Measured points')
    labelPlot()
    a, b = np.polyfit(f, d, 1)
    print('a =', a, 'b =', b)
    plt.plot(f, a * f + b, 'r', label='Linear fit, k = ' + str(round(1 / float(a), 5)))
    # c, d = lr(f, d)
    # print(c, d)
    # plt.plot(f, c * f + d, 'g', label='Linear fit, k = ' + str(round(1 / float(c), 5)))
    plt.legend(loc='best')
def fitData1(fileName):
    m, d = getData(fileName)
    m = np.array(m)
    d = np.array(d)
    f = m * 9.81  # get force
    plt.plot(f, d, 'bo', label='Measured points')
    labelPlot()
    model = np.polyfit(f, d, 1)
    est_vals = np.polyval(model, f)
    plt.plot(f, est_vals, 'r', label='Linear fit, k = ' + str(round(1 / model[0], 5)))
    plt.legend(loc='best')
def rSquared(observed, predicted):# [0, 1] useful for reporting to manager
    # Why aveMeanSquaredError(observed, predicted) is always < np.Var because
    # aveMeanSquareError(observed, predicted) is the smallest one because of predicted = Polyval(Polyfit(), xvals)
    # and np.var is aveMeanSquareError(observed, [mean]*len(observed))
    return 1 - (utils.aveMeanSquareError(observed, predicted) / np.var(observed))
def testFits(degrees, xVals, yVals, title):
    plt.plot(xVals, yVals, 'o', label='Data')
    for i in range(len(degrees)):
        model = np.polyfit(xVals, yVals, degrees[i])
        est_vals = np.polyval(model, xVals)
        error = rSquared(yVals, est_vals)
        plt.plot(xVals, est_vals, label='Fit of degree ' + str(degrees[i]) + ', R2 = ' + str(round(error, 5)))
    plt.legend(loc='best')
    plt.title(title)
def genNoisyParabolicData(a, b, c, xVals, fName):
    yVals = []
    for x in xVals:
        theoreticalVal = a * x ** 2 + b * x + c
        yVals.append(theoreticalVal + random.gauss(0, 35))
    f = open(fName, 'w')
    f.write('x        y\n')
    for i in range(len(yVals)):
        f.write(str(yVals[i]) + ' ' + str(xVals[i]) + '\n')
    f.close()

fitData('springData.txt')
plt.show()
fitData1('springData.txt')
plt.show()

'''
#                                             Demonstration using mystery data
'''
xVals, yVals = getData('mysteryData.txt')
plt.plot(xVals, yVals, 'o', label='Data Points')
plt.title('Mystery Data')
#                                                     Try linear model
model1 = np.polyfit(xVals, yVals, 1)
plt.plot(xVals, np.polyval(model1, xVals), label='Linear Model')
#                                                   Try a quadratic model
model2 = np.polyfit(xVals, yVals, 2)
plt.plot(xVals, np.polyval(model2, xVals), 'r--', label='Quadratic Model')
plt.legend()
plt.show()
#                                                       Compare models
#                                          code to compare fits for mystery data
estYVals = np.polyval(model1, xVals)
print('Ave. mean square error for linear model =', aveMeanSquareError(yVals, estYVals))
estYVals = np.polyval(model2, xVals)
print('Ave. mean square error for quadratic model =', aveMeanSquareError(yVals, estYVals))
'''

#                                     code for testing goodness of fit to parabolic data
'''
xVals, yVals = getData('mysteryData.txt')
degrees = (1, 2)
testFits(degrees, xVals, yVals, 'Mystery Data')
plt.show()

#                                                     Compare higher-order fits
degrees = (2, 4, 8, 16)
testFits(degrees, xVals, yVals, 'Mystery Data')
plt.savefig('Linear regression.png', dpi=300)
plt.show()
'''
'''
#                                             parameters for generating data
xVals = range(-10, 11, 1)
a, b, c = 3.0, 0.0, 0.0
degrees = (2, 4, 8, 16)

#                                                     generate data
random.seed(0)
genNoisyParabolicData(a, b, c, xVals, 'Dataset 1.txt')
genNoisyParabolicData(a, b, c, xVals, 'Dataset 2.txt')
#
xVals1, yVals1 = getData('Dataset 1.txt')
testFits(degrees, xVals1, yVals1, 'DataSet 1.txt')
plt.show()
'''
'''
class tempDatum(object):
    def __init__(self, s):
        info = s.split(',')
        self.high = float(info[1])
        self.year = int(info[2][0:4])

    def getHigh(self):
        return self.high

    def getYear(self):
        return self.year
def getTempData():
    inFile = open('temperatures.csv')
    inFile.readline()
    data = []
    for l in inFile:
        data.append(tempDatum(l))
    return data
def getYearlyMeans(data):
    years = {}
    for d in data:
        try:
            years[d.getYear()].append(d.getHigh())
        except:
            years[d.getYear()] = [d.getHigh()]
    for y in years:
        years[y] = sum(years[y]) / len(years[y])
    return years
def fitData3(fileName):
    m, d = getData(fileName)
    m = np.array(m)
    d = np.array(d)
    f = m * 9.81  # get force
    plt.plot(f, d, 'bo', label='Measured points')
    labelPlot()
    model = np.polyfit(f, d, 1)
    f = f + [2]
    d = d + []
    estYVals = np.polyval(model, f)
    plt.plot(f, estYVals, 'r', label='Linear fit, r**2 = ' + str(round(rSquared(yVals, estYVals), 5)))
    model = np.polyfit(f, d, 2)
    estYVals = np.polyval(model, f)
    plt.plot(f, estYVals, 'g--', label='Quadratic fit, r**2 = ' + str(round(rSquared(yVals, estYVals), 5)))
    plt.title('A Linear Spring')
    labelPlot()
    plt.legend(loc='best')
def splitData(xVals, yVals):
    toTrain = random.sample(range(len(xVals)), len(xVals) // 2)
    trainX, trainY, testX, testY = [], [], [], []
    for i in range(len(xVals)):
        if i in toTrain:
            trainX.append(xVals[i])
            trainY.append(yVals[i])
        else:
            testX.append(xVals[i])
            testY.append(yVals[i])
    return trainX, trainY, testX, testY

random.seed(0)
data = getTempData()
years = getYearlyMeans(data)
xVals, yVals = [], []
for e in years:
    xVals.append(e)
    yVals.append(years[e])
plt.plot(xVals, yVals)
plt.xlabel('Year')
plt.ylabel('Mean Daily High (C)')
plt.title('Select U.S. Cities')
plt.show()
#                                              UNCOVER FOR SECOND DEMO
numSubsets = 10
dimensions = (1, 2, 3, 4)
rSquares = {}
for d in dimensions:
       rSquares[d] = []
for f in range(numSubsets):
    trainX, trainY, testX, testY = splitData(xVals, yVals)
    for d in dimensions:
        model = np.polyfit(trainX, trainY, d)
        # estYVals = np.polyval(model, trainX)
        estYVals = np.polyval(model, testX)
        rSquares[d].append(rSquared(testY, estYVals))
print('Mean R-squares for test data')
for d in dimensions:
    mean = round(sum(rSquares[d])/len(rSquares[d]), 4)
    sd = round(np.std(rSquares[d]), 4)
    print('For dimensionality', d, 'mean =', mean, 'Std =', sd)
print(rSquares[1])
'''
########################################################################################################################
#                                              L8 SAMPLING AND STANDARD ERRORS
########################################################################################################################
'''
def makeHist(data, title, xlabel, ylabel, bins=20):
    pylab.hist(data, bins=bins)
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
def getHighs():
    inFile = open('temperatures.csv')
    population = []
    for l in inFile:
        try:
            population.append(float(l.split(',')[1]))
        except:
            continue
    return population
def getMeansAndSDs(population, sample, verbose=False):
    popMean = sum(population) / len(population)
    sampleMean = sum(sample) / len(sample)
    if verbose:
        makeHist(population,
                 'Daily High 1961-2015, Population\n' + \
                 '(mean = ' + str(round(popMean, 2)) + ')',
                 'Degrees C', 'Number Days')
        pylab.figure()
        makeHist(sample, 'Daily High 1961-2015, Sample\n' + \
                 '(mean = ' + str(round(sampleMean, 2)) + ')',
                 'Degrees C', 'Number Days')
        print('Population mean =', popMean)
        print('Standard deviation of population =',
              numpy.std(population))
        print('Sample mean =', sampleMean)
        print('Standard deviation of sample =',
              numpy.std(sample))
    return popMean, sampleMean, numpy.std(population), numpy.std(sample)
def showErrorBars(population, sizes, numTrials):
    popMean = sum(population)/len(population)
    xVals = []
    sizeMeans, sizeSDs = [], []
    for sampleSize in sizes:
        xVals.append(sampleSize)
        trialMeans = []
        for t in range(numTrials):
            sample = random.sample(population, sampleSize)
            popMean, sampleMean, popSD, sampleSD = getMeansAndSDs(population, sample)
            trialMeans.append(sampleMean)
        sizeMeans.append(sum(trialMeans) / len(trialMeans))
        sizeSDs.append(numpy.std(trialMeans))
    print(sizeSDs)
    pylab.errorbar(xVals, sizeMeans,
                   yerr=1.96 * pylab.array(sizeSDs), fmt='o',
                   label='95% Confidence Interval')
    pylab.title('Mean Temperature (' + str(numTrials) + ' trials)')
    pylab.xlabel('Sample Size')
    pylab.ylabel('Mean')
    pylab.axhline(y=popMean, color='r', label='Population Mean')
    pylab.xlim(0, sizes[-1] + 10)
    pylab.legend()
def sem(popSD, sampleSize):
    return popSD / sampleSize ** 0.5
def plotDistributions():
    uniform, normal, exp = [], [], []
    for i in range(100000):
        uniform.append(random.random())
        normal.append(random.gauss(0, 1))
        exp.append(random.expovariate(0.5))
    makeHist(uniform, 'Uniform', 'Value', 'Frequency')
    pylab.figure()
    makeHist(normal, 'Gaussian', 'Value', 'Frequency')
    pylab.figure()
    makeHist(exp, 'Exponential', 'Value', 'Frequency')
def getDiffs(population, sampleSizes):
    popStd = numpy.std(population)
    diffsFracs = []
    for sampleSize in sampleSizes:
        diffs = []
        for t in range(100):
            sample = random.sample(population, sampleSize)
            diffs.append(abs(popStd - numpy.std(sample)))
        diffMean = sum(diffs) / len(diffs)
        diffsFracs.append(diffMean / popStd)
    return pylab.array(diffsFracs) * 100
def plotDiffs(sampleSizes, diffs, title, label, color='b'):
    pylab.plot(sampleSizes, diffs, label=label, color=color)
    pylab.xlabel('Sample Size')
    pylab.ylabel('% Difference in SD')
    pylab.title(title)
    pylab.legend()
def compareDists():
    uniform, normal, exp = [], [], []
    for i in range(100000):
        uniform.append(random.random())
        normal.append(random.gauss(0, 1))
        exp.append(random.expovariate(0.5))
    sampleSizes = range(20, 600, 1)
    udiffs = getDiffs(uniform, sampleSizes)
    ndiffs = getDiffs(normal, sampleSizes)
    ediffs = getDiffs(exp, sampleSizes)
    plotDiffs(sampleSizes, udiffs,
              'Sample SD vs Population SD',
              'Uniform population', 'm')
    plotDiffs(sampleSizes, ndiffs,
              'Sample SD vs Population SD',
              'Normal population', 'b')
    plotDiffs(sampleSizes, ediffs,
              'Sample SD vs Population SD',
              'Exponential population', 'r')


population = getHighs()
popMean = sum(population)/len(population)
popSD = numpy.std(population)
random.seed(0)
sampleSizes = (25, 50, 100, 200, 300, 400, 500, 600, 1200, 2400)
numTrials = 50
population = getHighs()
sems = []
sampleSDs = []
sample1_means = []
for size in sampleSizes:
    sems.append(1.96*sem(popSD, size))
    sample1 = random.sample(population, size)
    means = []
    for t in range(numTrials):
        sample = random.sample(population, size)
        means.append(sum(sample)/len(sample))
    sample1_means.append(sum(sample1)/len(sample1))
    sampleSDs.append(1.96*numpy.std(means))

print(popMean, popSD, "\n", sample1_means, "\n", sems, "\n", sampleSDs)
temps = getHighs()
sampleSize = 200
numTrials = 10000
random.seed(0)
numBad = 0
for t in range(numTrials):
    start = random.choice(range(0, len(temps) - sampleSize))
    sample = temps[start:start+sampleSize]
    sampleMean = sum(sample)/sampleSize
    se = numpy.std(sample)/sampleSize**0.5
    print(numpy.std(sample), se, sampleMean)
    if abs(popMean - sampleMean) > 1.96*se:
        numBad += 1
print('Fraction outside 95% confidence interval =', numBad/numTrials)

random.seed(0)
numBad = 0
for t in range(numTrials):
   sample = random.sample(temps, sampleSize)
   sampleMean = sum(sample)/sampleSize
   se = numpy.std(sample)/sampleSize**0.5
   print(numpy.std(sample), se, sampleMean)
   if abs(popMean - sampleMean) > 1.96*se:
       numBad += 1
print(popMean, 'Fraction outside 95% confidence interval =', numBad/numTrials)
'''
########################################################################################################################
#                                 L6 MONTE CARLO SIMULATION  L7 CONFIDENCE INTERVALS
########################################################################################################################
'''
# set line width
pylab.rcParams['lines.linewidth'] = 4
# set font size for titles
pylab.rcParams['axes.titlesize'] = 20
# set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 20
# set size of numbers on x-axis
pylab.rcParams['xtick.labelsize'] = 16
# set size of numbers on y-axis
pylab.rcParams['ytick.labelsize'] = 16
# set size of ticks on x-axis
pylab.rcParams['xtick.major.size'] = 7
# set size of ticks on y-axis
pylab.rcParams['ytick.major.size'] = 7
# set size of markers, e.g., circles representing points
# set numpoints for legend
pylab.rcParams['legend.numpoints'] = 1

'''
'''
class FairRoulette():
    def __init__(self):
        self.pockets = list(range(1, 37))

    def betPocket(self, pocket, amt):
        ball = random.choice(self.pockets)
        print(ball)
        if str(pocket) == str(ball):
            return 35 * amt
        else:
            return -amt

    def __str__(self):
        return 'Fair Roulette'
class EuRoulette(FairRoulette):
    def __init__(self):
        FairRoulette.__init__(self)
        self.pockets.append(0)

    def __str__(self):
        return 'European Roulette'
class AmRoulette(EuRoulette):
    def __init__(self):
        EuRoulette.__init__(self)
        self.pockets.append(-1)

    def __str__(self):
        return 'American Roulette'
def run_trials_ret_list(game, numTrials, trialSize, toPrint):
    pocketReturns = []
    random.seed(0)
    for t in range(numTrials):
        trialVals = playRoulette_ret_mean(game, trialSize, 2, 1, toPrint)
        pocketReturns.append(trialVals)
    return pocketReturns
def playRoulette_ret_mean(game, numSpins, pocket, bet, toPrint=True):
    totPocket = 0
    for i in range(numSpins):
        totPocket += game.betPocket(pocket, bet)
    if toPrint:
        print(numSpins, 'spins of', game)
        print('Expected return betting', pocket, '=', str(100 * totPocket / numSpins) + '%\n')
    return (totPocket / numSpins)
def getMeanAndStd(X):
    mean = sum(X) / float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean) ** 2
    std = (tot / len(X)) ** 0.5
    return mean, std
def gaussian(x, mu, sigma):
    factor1 = (1.0 / (sigma * ((2 * pylab.pi) ** 0.5)))
    factor2 = pylab.e ** -(((x - mu) ** 2) / (2 * sigma ** 2))
    return factor1 * factor2
def checkEmpirical(numTrials):
    for t in range(numTrials):
        mu = random.randint(-10, 10)
        sigma = random.randint(1, 10)
        print('For mu =', mu, 'and sigma =', sigma)
        for numStd in (1, 1.96, 3):
            area = integrate.quad(gaussian, mu - numStd * sigma,
                                  mu + numStd * sigma, (mu, sigma))[0]
            print(' Fraction within', numStd, 'std =', round(area, 4))
def plotMeans(numDice, numRolls, numBins, legend, color, style):
    means = []
    for i in range(numRolls // numDice):
        vals = 0
        for j in range(numDice):
            vals += 5 * random.random()
        means.append(vals / float(numDice))
    # pylab.hist(means, numBins, color = color, label = legend, weights = [1/len(means)]len(means),
    #          hatch = style)
    return getMeanAndStd(means)
def throwNeedles(numNeedles):
    inCircle = 0.0
    for Needles in range(1, numNeedles + 1, 1):
        x = numpy.pi/3*random.random()
        y = random.random()
        if y < math.sin(x):
            inCircle += 1
    return  numpy.pi/3 * (inCircle / float(numNeedles))
def getEst(numNeedles, numTrials):
    estimates = []
    for t in range(numTrials):
        piGuess = throwNeedles(numNeedles)
        estimates.append(piGuess)
    sDev = numpy.std(estimates)
    curEst = sum(estimates) / len(estimates)
    print('Est. = ' + str(curEst) + ', Std. dev. = ' + str(sDev)
          + ', Needles = ' + str(numNeedles))
    return (curEst, sDev)
def estPi(precision, numTrials):
    numNeedles = 1000
    sDev = precision
    cur_est = 0
    while sDev >= precision / 2:
        cur_est, sDev = getEst(numNeedles, numTrials)
        numNeedles *= 2
    return cur_est

#L = []
#for i in range(10000):
#   L.append(random.gauss(0, 100))
#print(L, "\n", getMeanAndStd(L))

e = EuRoulette()
random.seed(0)
L1 = run_trials_ret_list(e, 100, 1000, True)
mean1, std1 = getMeanAndStd(L1)
L = []
random.seed(0)
for i in range(100000):
    L.append(e.betPocket(2, 1))
mean2, std2 = getMeanAndStd(L)
print(std2, std3)
print(mean1, std1**2, "\n", mean2, std2**2)  # mean1 ~= mean2 \\ 1000 * std1**2 ~= std2**2
tot = 0
for i in L1:
    if mean1 - 2*std1 <= i <= mean1 + 2*std1:
        tot += 1
print(tot/len(L1))
'''
'''
L = [random.choice([1, 2, 3, 4]) for j in range(20)]
prob = []
for i in range(2000000):
    r = 0
    for j in range(20):
        num = random.choice([1, 2, 3, 4])
        if L[j] == num:
            r += 1
    prob.append(1 if r >= 5 else 0)
print(prob, "\n", sum(prob)/len(prob))  # 0.585158 
'''
'''
n = 3
prob = []
for i in range(3000000):
    L = [random.choice(list(range(1, 38))) for j in range(37)]
    prob.append(1 if n in L else 0)
print(sum(prob)/len(prob))  # 0.63714865 = prob(there is at least 1 n in L) = 1-prob(there is no n in L)
'''
########################################################################################################################
#                                                 L5 RANDOM WALKS
########################################################################################################################
'''
class Drunk(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def dist_from(self, other):
        return ((self.get_x()-other.get_x())**2+(self.get_y()-other.get_y())**2)**0.5
    def move(self):
        c1, c2 = random.choice([(1, 0), (0, 1), (0, -1), (-1, 0)])
        self.x = self.x + c1
        self.y = self.y + c2
def test(num_steps, num_trials, drunk):
    distances = []
    for i in range(num_trials):
        temp = Drunk(drunk.get_x(), drunk.get_y())
        for j in range(num_steps):
            temp.move()
        distances.append(temp.dist_from(drunk))
    print("max distance", max(distances), "\nmin distance", min(distances), sep=" ")
    return sum(distances)/num_trials
d1 = Drunk(100, -8)
print(test(1000, 10000, d1))
'''
'''
class Location(object):
    def __init__(self, x, y):
        """x and y are numbers"""
        self.x = x
        self.y = y

    def move(self, deltaX, deltaY):
        """deltaX and deltaY are numbers"""
        return Location(self.x + deltaX, self.y + deltaY)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distFrom(self, other):
        xDist = self.x - other.getX()
        yDist = self.y - other.getY()
        return (xDist ** 2 + yDist ** 2) ** 0.5

    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'
class Field(object):
    def __init__(self):
        self.drunks = {}

    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc

    def moveDrunk(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        # use move method of Location to get new location
        self.drunks[drunk] = \
            self.drunks[drunk].move(xDist, yDist)

    def getLoc(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]
class Drunk(object):
    def __init__(self, name=None):
        """Assumes name is a str"""
        self.name = name

    def __str__(self):
        if self != None:
            return self.name
        return 'Anonymous'
class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return random.choice(stepChoices)
class MasochistDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0.0, 1.1), (0.0, -0.9),
                       (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)
def walk(f, d, numSteps):
    """Assumes: f a Field, d a Drunk in f, and numSteps an int >= 0.
       Moves d numSteps times, and returns the distance between
       the final location and the location at the start of the
       walk."""
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return start.distFrom(f.getLoc(d))
def simWalks(numSteps, numTrials, dClass):
    """Assumes numSteps an int >= 0, numTrials an int > 0,
         dClass a subclass of Drunk
       Simulates numTrials walks of numSteps steps each.
       Returns a list of the final distances for each trial"""
    Homer = dClass('Homer')
    origin = Location(0, 0)
    distances = []
    for t in range(numTrials):
        f = Field()
        f.addDrunk(Homer, origin)
        distances.append(round(walk(f, Homer, numSteps), 1))
    return distances
def drunkTest(walkLengths, numTrials, dClass):
    """Assumes walkLengths a sequence of ints >= 0
         numTrials an int > 0, dClass a subclass of Drunk
       For each number of steps in walkLengths, runs simWalks with
         numTrials walks and prints results"""
    for numSteps in walkLengths:
        distances = simWalks(numSteps, numTrials, dClass)
        print(dClass.__name__, 'random walk of', numSteps, 'steps')
        print(' Mean =', round(sum(distances) / len(distances), 4))
        print(' Max =', max(distances), 'Min =', min(distances))
def simAll(drunkKinds, walkLengths, numTrials):
    for dClass in drunkKinds:
        drunkTest(walkLengths, numTrials, dClass)

xVals = [1, 2, 3, 4]
yVals1 = [1, 2, 3, 4]
pylab.plot(xVals, yVals1, 'b-', label='first')
yVals2 = [1, 7, 3, 5]
pylab.plot(xVals, yVals2, 'r--', label='second')
pylab.legend()

class styleIterator(object):
    def __init__(self, styles):
        self.index = 0
        self.styles = styles

    def nextStyle(self):
        result = self.styles[self.index]
        if self.index == len(self.styles) - 1:
            self.index = 0
        else:
            self.index += 1
        return result
def simDrunk(numTrials, dClass, walkLengths):
    meanDistances = []
    for numSteps in walkLengths:
        print('Starting simulation of',
              numSteps, 'steps')
        trials = simWalks(numSteps, numTrials, dClass)
        mean = sum(trials) / len(trials)
        meanDistances.append(mean)
    return meanDistances
def simAll(drunkKinds, walkLengths, numTrials):
    styleChoice = styleIterator(('m-', 'b--', 'g-.'))
    for dClass in drunkKinds:
        curStyle = styleChoice.nextStyle()
        print('Starting simulation of', dClass.__name__)
        means = simDrunk(numTrials, dClass, walkLengths)
        pylab.plot(walkLengths, means, curStyle,
                   label=dClass.__name__)
    pylab.title('Mean Distance from Origin ('
                + str(numTrials) + ' trials)')
    pylab.xlabel('Number of Steps')
    pylab.ylabel('Distance from Origin')
    pylab.legend(loc='best')


random.seed(0)
numSteps = (10, 100, 1000, 10000, 100000)
simAll((UsualDrunk, MasochistDrunk), numSteps, 100)
pylab.plot(numSteps, pylab.array(numSteps)**0.5, 'k-.', label='Square root of steps')
pylab.plot(numSteps, pylab.array(numSteps)*0.05, 'g-.', label='numSteps*0.05')
pylab.legend(loc='best')
def getFinalLocs(numSteps, numTrials, dClass):
    locs = []
    d = dClass()
    for t in range(numTrials):
        f = OddField()
        f.addDrunk(d, Location(0, 0))
        for s in range(numSteps):
            f.moveDrunk(d)
        locs.append(f.getLoc(d))
    return locs
def plotLocs(drunkKinds, numSteps, numTrials):
    styleChoice = styleIterator(('k+', 'r^', 'mo'))
    for dClass in drunkKinds:
        locs = getFinalLocs(numSteps, numTrials, dClass)
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        xVals = pylab.array(xVals)
        yVals = pylab.array(yVals)
        meanX = sum(abs(xVals)) / len(xVals)
        meanY = sum(abs(yVals)) / len(yVals)
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle,
                   label=dClass.__name__ + \
                         ' mean abs dist = <'
                         + str(meanX) + ', ' + str(meanY) + '>')
    pylab.title('Location at End of Walks ('
                + str(numSteps) + ' steps)')
    pylab.ylim(-1000, 1000)
    pylab.xlim(-1000, 1000)
    pylab.xlabel('Steps East/West of Origin')
    pylab.ylabel('Steps North/South of Origin')
    pylab.legend(loc='lower center')
class OddField(Field):
    def __init__(self, numHoles=1000,
                 xRange=100, yRange=100):
        Field.__init__(self)
        self.wormholes = {}
        for w in range(numHoles):
            x = random.randint(-xRange, xRange)
            y = random.randint(-yRange, yRange)
            newX = random.randint(-xRange, xRange)
            newY = random.randint(-yRange, yRange)
            newLoc = Location(newX, newY)
            self.wormholes[(x, y)] = newLoc

    def moveDrunk(self, drunk):
        Field.moveDrunk(self, drunk)
        x = self.drunks[drunk].getX()
        y = self.drunks[drunk].getY()
        if (x, y) in self.wormholes:
            self.drunks[drunk] = self.wormholes[(x, y)]
def traceWalk(fieldKinds, numSteps):
    styleChoice = styleIterator(('b+', 'r^', 'ko'))
    for fClass in fieldKinds:
        d = UsualDrunk()
        f = fClass()
        f.addDrunk(d, Location(0, 0))
        locs = []
        for s in range(numSteps):
            f.moveDrunk(d)
            locs.append(f.getLoc(d))
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle,
                   label=fClass.__name__)
    pylab.title('Spots Visited on Walk ('
                + str(numSteps) + ' steps)')
    pylab.xlabel('Steps East/West of Origin')
    pylab.ylabel('Steps North/South of Origin')
    pylab.legend(loc='best')
# random.seed(0)
# plotLocs((UsualDrunk, MasochistDrunk), 10000, 1000)
# TraceWalk using oddField
# random.seed(0)
# traceWalk((Field, OddField), 500)
'''
########################################################################################################################
#                                             L4 Stochastic thinking
########################################################################################################################
'''
def roll_die():
    """returns a random int between 1 and 6"""
    return random.choice([1, 2, 3, 4, 5, 6])
def test_roll(n=10):
    result = ''
    for j in range(n):
        result = result + str(roll_die())
    print(result)
    return result
def run_sim(goal, num_trials):
    total = 0
    for i in range(num_trials):
        if test_roll(len(goal)) == goal:
            total += 1
    print('Actual probability of', goal, '=', round(1 / (6 ** len(goal)), 8))
    est_probability = round(total / num_trials, 8)
    print('Estimated Probability of', goal, '=', est_probability)
def same_date(num_people, num_same):
    possible_dates = range(366)
# possible_dates = 4*list(range(0, 57)) + [58] + 4*list(range(59, 366)) + 4*list(range(180, 270))
    birthdays = [0] * 366
    for p in range(num_people):
        birth_date = random.choice(possible_dates)
        birthdays[birth_date] += 1
    return max(birthdays) >= num_same
def birthdayProb(numPeople, numSame, numTrials):
    num_hits = 0
    for t in range(numTrials):
        if same_date(numPeople, numSame):
            num_hits += 1
    return num_hits, num_hits / numTrials


#run_sim('11111', 100000)
test_roll(5)
#random.seed(0)
for numPeople in [10, 20, 40, 100]:
    print('For', numPeople, 'est. prob. of a shared birthday is', birthdayProb(numPeople, 2, 100000))
    numerator = math.factorial(366)
    denom = (366 ** numPeople) * math.factorial(366 - numPeople)
    print('Actual prob. for (N =', numPeople, ') =', 1 - numerator / denom)
'''
########################################################################################################################
#                                            L3 Graph-theoretic models
########################################################################################################################
'''

class Node(object):
    def __init__(self, name):
        """Assumes name is a string"""
        self.name = name

    def getName(self):
        return self.name

    def __str__(self):
        return self.name
class Edge(object):
    def __init__(self, src, dst):
        """Assumes src and dst are nodes"""
        self.src = src
        self.dst = dst

    def getSource(self):
        return self.src

    def getDestination(self):
        return self.dst

    def __str__(self):
        return self.src.getName() + '->' + self.dst.getName()
class Digraph(object):
    """edges is a dict mapping each node to a list of
    its children"""

    def __init__(self):
        self.edges = {}

    def addNode(self, node):
        if node in self.edges:
            raise ValueError('Duplicate node')
        else:
            self.edges[node] = []

    def addEdge(self, edge):
        src = edge.getSource()
        dst = edge.getDestination()
        if not (src in self.edges and dst in self.edges):
            raise ValueError('Node not in graph')
        self.edges[src].append(dst)

    def childrenOf(self, node):
        return self.edges[node]

    def hasNode(self, node):
        return node in self.edges

    def getNode(self, name):
        for n in self.edges:
            if n.getName() == name:
                return n
        raise NameError(name)

    def __str__(self):
        result = ''
        for src in self.edges:
            for dst in self.edges[src]:
                result = result + src.getName() + '->' \
                         + dst.getName() + '\n'
        return result[:-1]  # omit final newline
class Graph(Digraph):
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)

G = Digraph()
for name in ["Yerevan", "Gyumri", "Stepanakert"]:
    G.addNode(Node(name))
G.addEdge(Edge(G.getNode("Yerevan"), G.getNode("Gyumri")))
G.addEdge(Edge(G.getNode("Yerevan"), G.getNode("Stepanakert")))
G.addEdge(Edge(G.getNode("Stepanakert"), G.getNode("Yerevan")))
G.addEdge(Edge(G.getNode("Gyumri"), G.getNode("Yerevan")))
print(G)


def buildCityGraph(graphType):
    g = graphType()
    for name in ('Boston', 'Providence', 'New York', 'Chicago',
                 'Denver', 'Phoenix', 'Los Angeles'):  # Create 7 nodes
        g.addNode(Node(name))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('Providence')))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('Boston')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('New York'), g.getNode('Chicago')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Denver')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Los Angeles'), g.getNode('Boston')))
    return g
def printPath(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result
def DFS(graph, start, end, path, shortest, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes;
          path and shortest are lists of nodes
       Returns a shortest path from start to end in graph"""
    path = path + [start]
    if toPrint:
        print('Current DFS path:', printPath(path))
    if start == end:
        return path
    for node in graph.childrenOf(start):
        if node not in path:  # avoid cycles
            if shortest == None or len(path) < len(shortest):
                newPath = DFS(graph, node, end, path, shortest,
                              toPrint)
                if newPath != None:
                    print(printPath(newPath))
                    shortest = newPath
        elif toPrint:
            print('Already visited', node)
    return shortest
printQueue = True
def BFS(graph, start, end, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    initPath = [start]
    pathQueue = [initPath]
    while len(pathQueue) != 0:
        # Get and remove oldest element in pathQueue
        if printQueue:
            print('Queue:', len(pathQueue))
            for p in pathQueue:
                print(printPath(p))
        tmpPath = pathQueue.pop(0)
        if toPrint:
            print('Current BFS path:', printPath(tmpPath))
            print()
        lastNode = tmpPath[-1]
        if lastNode == end:
            return tmpPath
        for nextNode in graph.childrenOf(lastNode):
            if nextNode not in tmpPath:
                newPath = tmpPath + [nextNode]
                pathQueue.append(newPath)
    return None
def shortest_path_dfs(graph, start, end, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return DFS(graph, start, end, [], None, toPrint)
def shortest_path_bfs(graph, start, end, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return BFS(graph, start, end, toPrint)
def test_sp(source, destination):
    g = buildCityGraph(Digraph)
    sp = shortest_path_bfs(g, g.getNode(source), g.getNode(destination), toPrint=True)
    if sp != None:
        print('Shortest path from', source, 'to', destination, 'is', printPath(sp))
    else:
        print('There is no path from', source, 'to', destination)


test_sp('Chicago', 'Boston')
print()
test_sp('Boston', 'Phoenix')
'''
########################################################################################################################
#                             L2   KNAPSACK PROBLEM GREEDY ALGORITHM DYNAMIC PROGRAMMING
########################################################################################################################
'''
def fastFib(n, memo={}):
    """Assumes n is an int >= 0, memo used only by recursive calls
       Returns Fibonacci of n"""
    if n == 0 or n == 1:
        return 1
    try:
        return memo[n]
    except KeyError:
        memo[n] = fastFib(n - 1, memo) + fastFib(n - 2, memo)
        return memo[n]
for i in range(121):
    print('fib(' + str(i) + ') =', fastFib(i))
'''
'''
class Food(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w
    def getValue(self):
        return self.value
    def getCost(self):
        return self.calories
    def density(self):
        return self.getValue()/self.getCost()
    def __str__(self):
        return self.name + ': <' + str(self.value)  + ', ' + str(self.calories) + '>'
def buildMenu(names, values, calories):
    """names, values, calories lists of same length.
       name a list of strings
       values and calories lists of numbers
       returns list of Foods"""
    mu = []
    for i in range(len(values)):
        mu.append(Food(names[i], values[i], calories[i]))
    return mu
def build_large_menu(num_items, max_value, max_cost):
    result = []
    for i in range(1, num_items+1):
        result.append(Food(str(i), random.randint(1, max_value), random.randint(1, max_cost)))
    return result
def greedy(items, maxCost, keyFunction):
    """Assumes items a list, maxCost >= 0,
         keyFunction maps elements of items to numbers"""
    itemsCopy = sorted(items, key=keyFunction, reverse=True)
    result = []
    totalValue, totalCost = 0.0, 0.0
    for i in range(len(itemsCopy)):
        if (totalCost+itemsCopy[i].getCost()) <= maxCost:
            result.append(itemsCopy[i])
            totalCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()
    return (result, totalValue)
def testGreedy(items, constraint, keyFunction):
    taken, val = greedy(items, constraint, keyFunction)
    print('Total value of items taken =', val)
    for item in taken:
        print('   ', item)
def testGreedys(foods, maxUnits):
    print('Use greedy by value to allocate', maxUnits, 'calories')
    testGreedy(foods, maxUnits, Food.getValue)
    print('\nUse greedy by cost to allocate', maxUnits, 'calories')
    testGreedy(foods, maxUnits, lambda x: 1/Food.getCost(x))
    print('\nUse greedy by density to allocate', maxUnits, 'calories')
    testGreedy(foods, maxUnits, Food.density)
def maxVal(toConsider, avail):
    """Assumes toConsider a list of items, avail a weight
       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and the items of that solution"""
    if toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].getCost() > avail:
        #Explore right branch only
        result = maxVal(toConsider[1:], avail)
    else:
        nextItem = toConsider[0]
        #Explore left branch
        withVal, withToTake = maxVal(toConsider[1:],
                                     avail - nextItem.getCost())
        withVal += nextItem.getValue()
        #Explore right branch
        withoutVal, withoutToTake = maxVal(toConsider[1:], avail)
        #Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    return result
def testMaxVal(foods, maxUnits, algorithm, printItems=True):
    print('Menu contains', len(foods), 'items')
    print('Use search tree to allocate', maxUnits,
          'calories')
    val, taken = algorithm(foods, maxUnits)
    if printItems:
        print('Total value of items taken =', val)
        for item in taken:
            print('   ', item)
def fastMaxVal(toConsider, avail, memo={}):
    """Assumes toConsider a list of subjects, avail a weight
         memo supplied by recursive calls
       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and the subjects of that solution"""
    if (len(toConsider), avail) in memo:
        result = memo[(len(toConsider), avail)]
    elif toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].getCost() > avail:
        # Explore right branch only
        result = fastMaxVal(toConsider[1:], avail, memo)
    else:
        nextItem = toConsider[0]
        # Explore left branch
        withVal, withToTake = fastMaxVal(toConsider[1:], avail - nextItem.getCost(), memo)
        withVal += nextItem.getValue()
        # Explore right branch
        withoutVal, withoutToTake = fastMaxVal(toConsider[1:],
                                               avail, memo)
        # Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    memo[(len(toConsider), avail)] = result
    return result


names = ['wine', 'beer', 'pizza', 'burger', 'fries', 'cola', 'apple', 'donut', 'cake']
values = [89, 90, 95, 100, 90, 79, 50, 10]
calories = [123, 154, 258, 354, 365, 150, 95, 195]
foods = buildMenu(names, values, calories)
l_foods = build_large_menu(35, 130, 250)
testGreedys(l_foods, 750)
print('')
testMaxVal(l_foods, 750, fastMaxVal, True)

'''
########################################################################################################################
#                                  6.0001 MIT COURSE INTRO TO COMPUTER SCIENCE AND PYTHON
########################################################################################################################
#                                                 BISECTION SEARCH CUBE ROOT
'''
cube = float(input("enter a number"))
low = 0
high = cube
if -1 < cube < 1:
    high = 1
if cube < 0:
    low = -abs(high)
    high = 0
eps = 0.01
guess = 0.0
num_guesses = 0
while abs(guess**3-cube) >= eps:
    if guess**3 < cube:
        low = guess
    else:
        high = guess
    guess = (high+low)/2.0
    print(guess)
    num_guesses += 1
print("num_guess = ", num_guesses)
print(guess, "is in", eps, "range of the cube root of", cube)
print("difference =",  guess**3-cube)'''
#                                                      TOWERS OF HANOI
'''

def print_move(fr, to):
    print("From", fr, "to", to)


def towers(n, fr, to, sp):
    if n == 1:
        print_move(fr, to)
    else:
        towers(n-1, fr, sp, to)
        towers(1, fr, to, sp)
        towers(n-1, sp, to, fr)


towers(3, "A", "B", "C") '''
#                                       FIBONACCI NUMBERS DYNAMIC RECURSION
'''

def fibonacci(x, l):
    if l[x] != 0:
        return l[x]
    l[x] = fibonacci(x-1, l) + fibonacci(x-2, l)
    return l[x]


List = 1000*[0]
List[0] = List[1] = 1
print(fibonacci(990, List))'''
#                                                    PALINDROME STRINGS
'''def tochars(s):
    s = s.lower()
    ans = ""
    for i in s:
        if i in "asdfghjklqwertyuiopzxcvbnm":
            ans = ans + i
    return ans
def is_palindrome(s):
    if len(s) <= 1:
        return True
    return s[0] == s[-1] and is_palindrome(s[1:-1])
#   return s == s[::-1]
str = input("Enter a string")
if is_palindrome(tochars(str)):
    print("It's a palindrome")
else:
    print("It's not a palindrome")
'''
#                                                  DICTIONARY PROBLEMS
'''
def lyrics_to_freq(lyrics):
    my_dict = {}
    lyrics = lyrics.split()
    for word in lyrics:
        if word in my_dict:
            my_dict[word] += 1
        else:
            my_dict[word] = 1
    return my_dict

def most_common_words(freq):
    values = freq.values()
    best = max(values)
    words = []
    for word in freq:
        if freq[word] == best:
            words.append(word)
    return (words, best)

def words_often(lyrics, min_times):
    result = []
    temp = most_common_words(lyrics)
    while temp[1] >= min_times:
        result.append(temp)
        for a in temp[0]:
            del(lyrics[a])
        temp = most_common_words(lyrics)
    return result


beatles = "f f I am a sugar . Don't go against sugar unless I f f am a solt. sugar"
print(words_often(lyrics_to_freq(beatles), 2))
print(beatles)
'''
#                                              TRY EXCEPT ELSE FINALLY ASSERT
'''
def avg(list):
    assert len(list) != 0, "no grades data"
    return sum(list)/len(list)

def square_root(num):
#   assert num >= 0, "Negative value was entered"
    if num < 0:
        print("Negative value was entered")
    else:
        return num**0.5
def avg(list):
    try:
        return sum(list)/len(list)
    except ZeroDivisionError:
        print("warning: no grades data")
        return 0.0

def  get_stats(lt):
    new_stats = []
    for el in lt:
        new_stats.append([el[0], el[1], avg(el[1])])
    return new_stats


print(square_root(-9))
test_grades = [[["Peter", "Parker"], []], [["Bruce", "Wayne"], [100.0, 80.0, 74.0]]]
print(get_stats(test_grades))
t = True
while t:
    try:
        a = int(input("Enter a number"))
        b = int(input("Enter a number"))
        print("a/b = ", a/b)
        print("a+b = ", a+b)
        t = False
    except ValueError:
        print("Could not convert to a number")
    except ZeroDivisionError:
        print("Can't divide by zero")
    except:
        print("Something went very wrong")
    else:
        print("No exceptions found")
    finally:
        print("Program finished")
'''

#                                                   CLASS COORDINATE
'''

class Coordinate(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other): return self.x == other.x and self.y == other.y

    def __str__(self): return "(" + str(self.x) + "," + str(self.y) + ")"

    def dist_from_zero(self): return (self.x**2+self.y**2)**0.5

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx ** 2 + dy ** 2) ** 0.5

    def __sub__(self, other): return Coordinate(self.x-other.x, self.y-other.y)

    def __add__(self, other): return Coordinate(self.x+other.x, self.y+other.y)


A = Coordinate(3, 4)
B = Coordinate(9, 12)
C = Coordinate(11, 10)
print("A-", A, A.dist_from_zero(), "\nB-", B, B.dist_from_zero(), "\nC-", C, C.dist_from_zero())
print((C-A).dist_from_zero() == (B-A).dist_from_zero())
print(A.distance(B) == A.distance(C))
print("Distance between A", A, " and B", B, " is ", Coordinate.distance(B, A), sep="")
print(isinstance(A, Coordinate))
'''
#                                                 CLASS FRACTION
'''

class Fraction(object):
    def __init__(self, num=0, denom=1):
        assert type(num) == int and type(denom) == int, "Type error"
        self.num = num
        self.denom = denom

    def __str__(self): return str(self.num) + "/" + str(self.denom)

    def __add__(self, other): return Fraction(self.num * other.denom + self.denom * other.num, self.denom * other.denom)

    def __sub__(self, other): return Fraction(self.num * other.denom - self.denom * other.num, self.denom * other.denom)

    def __float__(self): return self.num/self.denom

    def invert(self): return Fraction(self.denom, self.num)


A = Fraction(5, 8)
B = Fraction(3, 4)
C = A + B
print("", A, B, C, "\n", float(A), float(B), float(C))
'''
#                                             CLASSES  INHERITANCE
#                                          Animal abstract data type
'''
class Animal(object):
    def __init__(self, age):
        self.age = age
        self.name = None

    def get_age(self):
        return self.age

    def get_name(self):
        return self.name

    def set_age(self, newage):
        self.age = newage

    def set_name(self, newname=""):
        self.name = newname

    def __str__(self):
        return "animal:" + str(self.name) + ":" + str(self.age)


print("\n---- animal tests ----")
a = Animal(4)
print(a)
print(a.get_age())
a.set_name("fluffy")
print(a)
a.set_name()
print(a)

#################################
#                                        Inheritance example CAT


class Cat(Animal):
    def speak(self):
        print("meow")

    def __str__(self):
        return "cat:" + str(self.name) + ":" + str(self.age)


print("\n---- cat tests ----")
c = Cat(5)
c.set_name("fluffy")
print(c)
c.set_age(14)
c.speak()
print(c)
# a.speak() # error because there is no speak method for Animal class

#################################
#                                           Inheritance example       PERSON


class Person(Animal):
    def __init__(self, name, age):
        Animal.__init__(self, age)
        self.set_name(name)
        self.friends = []

    def get_friends(self):
        return self.friends

    def speak(self):
        print("hello")

    def add_friend(self, fname):
        if fname not in self.friends:
            self.friends.append(fname)

    def age_diff(self, other):
        diff = self.age - other.age
        print(abs(diff), "year difference")

    def __str__(self):
        return "person:" + self.name + ":" + str(self.age)


print("\n---- person tests ----")
p1 = Person("jack", 30)
p2 = Person("jill", 25)
print(p1.get_name())
print(p1.get_age())
print(p2.get_name())
print(p2.get_age())
print(p1)
p1.speak()
p1.age_diff(p2)


#################################
#                                            Inheritance example   STUDENT(PERSON)

class Student(Person):
    def __init__(self, name, age, major=None):
        Person.__init__(self, name, age)
        self.major = major

    def __str__(self):
        return "student:" + str(self.name) + ":" + str(self.age) + ":" + str(self.major)

    def change_major(self, major):
        self.major = major

    def speak(self):
        r = random.random()
        if r < 0.25:
            print("i have homework")
        elif 0.25 <= r < 0.5:
            print("i need sleep")
        elif 0.5 <= r < 0.75:
            print("i should eat")
        else:
            print("i am watching tv")


print("\n---- student tests ----")
s1 = Student('alice', 20, "CS")
s2 = Student('beth', 18)
print(s1)
print(s2)
print(s1.get_name(), "says:", end=" ")
s1.speak()
print(s2.get_name(), "says:", end=" ")
s2.speak()


#################################
#                                        Use of class variables  RABBIT

class Rabbit(Animal):
    # a class variable, tag, shared across all instances
    tag = 1

    def __init__(self, age, parent1=None, parent2=None):
        Animal.__init__(self, age)
        self.parent1 = parent1
        self.parent2 = parent2
        self.rid = Rabbit.tag
        Rabbit.tag += 1

    def get_rid(self):
        # zfill used to add leading zeroes 001 instead of 1
        return str(self.rid).zfill(3)

    def get_parent1(self):
        return self.parent1

    def get_parent2(self):
        return self.parent2

    def __add__(self, other):
        # returning object of same type as this class
        return Rabbit(0, self, other)

    def __eq__(self, other):
        parents_same = self.parent1.rid == other.parent1.rid \
                       and self.parent2.rid == other.parent2.rid
        parents_opposite = self.parent2.rid == other.parent1.rid \
                           and self.parent1.rid == other.parent2.rid
        return parents_same or parents_opposite

    def __str__(self):
        return "rabbit:" + self.get_rid() + "\t\tname:" + str(self.get_name()) + "\t\tage:" + str(self.get_age())


print("\n---- rabbit tests ----")
r1 = Rabbit(3)
r2 = Rabbit(4)
r1.set_name("Arthur")
r2.set_name("Anna")
print("r1:", r1)
print("r2:", r2)
print("r1 parent1:", r1.get_parent1())
print("r1 parent2:", r1.get_parent2())
r3 = r1.__add__(r2)
print("r3:", r3)
print("r3 parent1:", r3.get_parent1())
print("r3 parent2:", r3.get_parent2())
r4 = r2 + r1
print("r4 parent1:", r4.get_parent1())
print("r4 parent2:", r4.get_parent2())
print("r3 and r4 have same parents?", r3 == r4)
'''
#                                                BISECTION SEARCH
'''

def bisect_search(L, n):
    def bisect_search_helper(L, n, low, high):
        if low == high:
            return L[low] == n
        mid = (low + high)//2
        print("mid:", mid, "value:", L[mid])
        if L[mid] == n:
            return True
        if L[mid] > n:
            if mid == low:
                return False
            print(L[low:mid])
            return bisect_search_helper(L, n, low, mid-1)
        print(L[mid + 1: high+1])
        return bisect_search_helper(L, n, mid+1, high)
    if len(L) == 0:
        return False
    return bisect_search_helper(L, n, 0, len(L)-1)


L = [45, 78, 12, 70, 73, 90, 91, 93, 88, 82, 61, 34, 36, 20, 44, 66, 99, 58, 19, 38, 33, 37, 48, 59, 77, 24, 96, 23, 50]
L.sort()
print(L, len(L))
print(bisect_search(L, 88))
'''
#                                          SUBSETS OF A SET EXPONENTIAL
'''

def get_subsets(L):
    if len(L) == 0:
        return [[]]
    smaller = get_subsets(L[:-1])
    new = []
    for small in smaller:
        new.append(small + L[-1:])
    return smaller + new


L = [1, 2, 3, 4]
P = [77, 88]
P.extend(L)
P = P + L
print(P)
print(get_subsets(L))
'''
#                                         BUBBLE SELECTION MERGE SORTS
'''

def bubble_sort(P):
    c = False
    while not c:
        c = True
        for i in range(1, len(P)):
            if P[i-1] > P[i]:
                P[i-1], P[i] = P[i], P[i-1]
                c = False
    return P


def selection_sort(P):
    index = 0
    while index != len(P)-1:
        for i in range(index+1, len(P)):
            if P[i] < P[index]:
                P[i], P[index] = P[index], P[i]
        index += 1
    return P


def merge_sort(P):
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        while i != len(left):
            result.append(left[i])
            i += 1
        while j != len(right):
            result.append(right[j])
            j += 1
        return result
    if len(P) == 1:
        return P
    else:
        mid = len(P)//2
        l = merge_sort(P[:mid])
        r = merge_sort(P[mid:])
        return merge(l, r)


L = [12, 4, 785, 36, 24, 0, 77, 156, 59, 97]

print(bubble_sort(L))
print(selection_sort(L))
print(merge_sort(L))
'''