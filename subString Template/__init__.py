"""
backtracing
"""
def helper(lst, n):
    if n == 0: return [0]
    if n == 1: return lst
    if len(lst) < n:
        return []
    else:
        return helper(lst[1:], n) + [lst[0] + i for i in helper(lst[1:], n - 1)]


print(helper([1,2,4,8], 3))
