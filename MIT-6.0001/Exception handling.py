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
