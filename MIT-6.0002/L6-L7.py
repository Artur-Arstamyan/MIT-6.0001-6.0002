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
