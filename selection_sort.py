def selection_sort(A):
    for i in range(len(A)):
        m = i 
        for j in range(i):
            if A[m] < A[j]:
                m = j 
        A[m], A[i] = A[i], A[m]
        