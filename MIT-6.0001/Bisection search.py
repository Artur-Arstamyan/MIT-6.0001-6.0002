#                                                BISECTION SEARCH
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
