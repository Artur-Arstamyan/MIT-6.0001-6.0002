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
