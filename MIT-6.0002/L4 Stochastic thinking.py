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
