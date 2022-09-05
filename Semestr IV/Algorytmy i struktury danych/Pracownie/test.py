import numpy as np
from tqdm.auto import tqdm
from itertools import chain, combinations
from numpy.linalg import matrix_power
from math import gcd

def factors(x):
    l = []
    for i in range(1, x + 1):
        if x % i == 0:
            l.append(i)
    return l

def fast_matrix_mod_exp(M,n,m):
    W = np.identity(M.shape[0]).astype(int)
    if n==0:
        return W
    while n>1:
        if n % 2 == 1:
            W = np.matmul(M,W) % m
        M = np.matmul(M,M) % m
        n = n // 2
    return np.matmul(W,M) % m

def f():
    m = np.arange(16).reshape((4,4))
    print(m)
    return m.T
if __name__ == "__main__":
    m = f()
    print(m)

    # M = np.random.randint(0,2,(3,3)).astype(int)
    # print(M)
    # # n=4
    # m=30
    # for m in range(2,10):
    #     done = False
    #     l = []
    #     for n in range(1000):
    #         temp = fast_matrix_mod_exp(M, n, m)
    #         for prev in l:
    #             if (prev==temp).all():
    #                 print(m,n)
    #                 done=True
    #                 break
    #         l.append(temp)
    #         if done:
    #             break