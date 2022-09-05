import numpy as np


def alg(A,B,C):
    if A.shape[0] == 0 or B.shape[0] == 0 or C.shape[0] == 0:
        return [A,B,C]
    a = A[(A.shape[0])//2]
    b = B[(B.shape[0])//2]
    c = C[(C.shape[0])//2]
    if a < b:
        if a < c:
            L1 = A.copy()
            if b < c:
                L2 = B.copy()
                L3 = C.copy()
            else:
                L2 = C.copy()
                L3 = B.copy()
        else:
            L1 = C.copy()
            L2 = A.copy()
            L3 = B.copy()
    else:
        if a < c:
            L1 = B.copy()
            L2 = A.copy()
            L3 = C.copy()
        else:
            if c < b:
                L1 = C.copy()
                L2 = B.copy()
                L3 = A.copy()
            else:
                L1 = B.copy()
                L2 = C.copy()
                L3 = A.copy()
    n = min(L1.shape[0]//2,L3.shape[0]//2)
    return alg(L1[n-1:],L2,L3[:n+1])

def alg2(L,j):
    m = np.zeros(len(L))
    minimum = -np.inf
    maximum = np.inf
    minimum_index = 0
    maximum_index = 0
    for i in range(len(L)):
        m[i] = np.median(np.array(L[i]))
        if minimum > m[i]:
            minimum_index = i
            minimum = m[i]
        if maximum < m[i]:
            maximum_index = i
            maximum = m[i]

    cutting_point = min(len(L[minimum_index])//2,len(L[maximum_index])//2)
    L[minimum_index] = L[minimum_index][cutting_point:]
    L[maximum_index] = L[maximum_index][:cutting_point]
    print("\n",i)
    for l in L:
        print(l)

    alg2(L,j+1)


if __name__=="__main__":
    A = [2,3,6,8,10,11]
    B = [1,7,9,11,21,22]
    C = [1,2,9,11,16,17]
    D = [8,12,14,16,18,19]
    L = [A,B,C,D]
    # alg2(L,0)
    m = np.hstack([A,B,C,D])
    print(sorted(m))
    print(len(m))