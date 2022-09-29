import numpy as np


def pierwiastek(n):
    # specification: function calculate floor of a square root of a given number
    # input type: int; greater or equal to 0
    # output type: int

    partial_sum = 0
    i = 1
    while partial_sum <= n:
        partial_sum += (2 * i - 1)
        i += 1
    return i - 2

"""
k^2 = \sum_{i=1}^k (2i-1)
My algorithm is based on the observation, that to calculate floor of
sqrt of a given number I can just check for which i sum will exceed it.
Then wanted value is i - 1.
Algorithm works in time O(sqrt(N)), which is not the best. We can do better
simply by bisection method - O(log(n)).
"""


if __name__ == '__main__':
    for i in range(100):
        assert pierwiastek(i) == int(np.floor(np.sqrt(i)))
