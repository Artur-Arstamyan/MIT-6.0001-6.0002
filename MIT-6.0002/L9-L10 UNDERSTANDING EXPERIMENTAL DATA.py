# my own polyfit
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

#                                             Demonstration using mystery data
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

#                                     code for testing goodness of fit to parabolic data
xVals, yVals = getData('mysteryData.txt')
degrees = (1, 2)
testFits(degrees, xVals, yVals, 'Mystery Data')
plt.show()

#                                                     Compare higher-order fits
degrees = (2, 4, 8, 16)
testFits(degrees, xVals, yVals, 'Mystery Data')
plt.savefig('Linear regression.png', dpi=300)
plt.show()


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
