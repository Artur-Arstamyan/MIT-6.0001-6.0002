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
