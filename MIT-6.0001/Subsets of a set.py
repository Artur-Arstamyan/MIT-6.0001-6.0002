#                                          SUBSETS OF A SET(EXPONENTIAL TIME COMPLEXITY)
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
