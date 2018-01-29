def median_of_medians(A, i):

    #divide A into sublists of len 5

    sublists = [A[j:j+5] for j in range(0, len(A), 5)]

    medians = [sorted(sublist)[len(sublist)//2] for sublist in sublists]

    if len(medians) <= 5:
        pivot = sorted(medians)[len(medians)//2]
    else:
        #the pivot is the median of the medians
        pivot = median_of_medians(medians, len(medians)//2)

    #partitioning step
    low = [j for j in A if j < pivot]
    high = [j for j in A if j > pivot]

    k = len(low)
    if i < k:
        return median_of_medians(low,i)
    elif i > k:
        return median_of_medians(high,i-k-1)
    else: #pivot = k
        return pivot

"""
find-kth(A, k)
  B = [median(A[1], .., A[5]), median(A[6], .., A[10]), ..]
  pivot = find-kth(B, |B|/2)
"""

print(median_of_medians([1,2,5,4,3], 3))
from sklearn.cluster import KMeans