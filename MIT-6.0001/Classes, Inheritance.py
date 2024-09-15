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
