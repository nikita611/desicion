def MergeSort(A=[]):
    if len(A) > 1:
        m = len(A) // 2
        return Merge(MergeSort(A[0:m]), MergeSort(A[m:]))
    else:
        return A


def Merge(A=[], B=[]):
    res = []
    while True:
        if len(A) == 0:
            res.extend(B)
            break
        if len(B) == 0:
            res.extend(A)
            break
        if A[0] < B[0]:
            res.append(A.pop(0))
        else:
            res.append(B.pop(0))
    return res

list = list(map(int, input().split()))
sort_list = MergeSort(list)
print(sort_list)