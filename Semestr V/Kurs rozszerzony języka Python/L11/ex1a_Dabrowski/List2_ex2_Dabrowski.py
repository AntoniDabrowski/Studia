import numpy as np
import doctest


class ArgumentNotIntError(Exception):
    pass


def pierwiastek(n):
    """
    Function calculate floor of a square root of a given number
    Examples:
    >>> [pierwiastek(n) for n in [3,13,23]]
    [1, 3, 4]
    >>> pierwiastek(64)
    8
    >>> pierwiastek("64")
    Traceback (most recent call last):
    ...
    List2_ex2_Dabrowski.ArgumentNotIntError
    """
    if type(n) != int:
        raise ArgumentNotIntError

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
    # auto-documentation:
    # Docs\_build\html\index.html

    # testing
    doctest.testmod()

    # Running example
    # for i in range(100):
    #     assert pierwiastek(i) == int(np.floor(np.sqrt(i)))
