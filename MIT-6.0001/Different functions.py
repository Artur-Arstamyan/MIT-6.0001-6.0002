#                               FINDING CUBE ROOT OF THE INPUT WITH GIVEN MAX ERROR BY BISECTION SEARCH
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
print("difference =",  guess**3-cube)
'''
#                                                      TOWERS OF HANOI
def print_move(fr, to):
    print("From", fr, "to", to)

def towers(n, fr, to, sp):
    if n == 1:
        print_move(fr, to)
    else:
        towers(n-1, fr, sp, to)
        towers(1, fr, to, sp)
        towers(n-1, sp, to, fr)

towers(3, "A", "B", "C")

#                                       FIBONACCI NUMBERS DYNAMIC RECURSION
def fibonacci(x, l):
    if l[x] != 0:
        return l[x]
    l[x] = fibonacci(x-1, l) + fibonacci(x-2, l)
    return l[x]

List = 1000*[0]
List[0] = List[1] = 1
print(fibonacci(990, List))
#                                                    PALINDROME STRINGS
def tochars(s):
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
#                                                  DICTIONARY PROBLEMS
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
