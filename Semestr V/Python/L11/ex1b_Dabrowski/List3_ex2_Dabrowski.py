import doctest

class ArgumentNotIntError(Exception):
    pass

def perfect_imperative(n):
    """
    Function return list of perfect numbers less than or equal to n.
    Examples:
    >>> perfect_imperative(800)
    [6, 28, 496]
    >>> perfect_imperative(1)
    []
    >>> perfect_imperative(-222)
    []
    >>> perfect_imperative("64")
    Traceback (most recent call last):
    ...
    List3_ex2_Dabrowski.ArgumentNotIntError
    """

    if type(n) != int:
        raise ArgumentNotIntError

    def is_perfect(k):
        # input type: integer
        # output type: boolean
        # specification: Test whether n is perfect
        if k < 6:
            return False
        s = 0
        for j in range(1, k):
            if k % j == 0:
                s += j
        return s == k

    if n < 6:
        return []
    i = 6
    result = []
    while i <= n:
        if is_perfect(i):
            result.append(i)
        i += 1
    return result


def perfect_comprehension(n):
    """
    Function return list of perfect numbers less than or equal to n.
    Examples:
    >>> perfect_comprehension(800)
    [6, 28, 496]
    >>> perfect_comprehension(1)
    []
    >>> perfect_comprehension(-222)
    []
    >>> perfect_comprehension("64")
    Traceback (most recent call last):
    ...
    List3_ex2_Dabrowski.ArgumentNotIntError
    """

    if type(n) != int:
        raise ArgumentNotIntError

    return [i for i in range(2, n + 1) if
            [a for a in [0] for j in [k for k in range(1, i) if i % k == 0] for a in [a + j]][-1] == i]


def perfect_functional(n):
    """
    Function return list of perfect numbers less than or equal to n.
    Examples:
    >>> perfect_functional(800)
    [6, 28, 496]
    >>> perfect_functional(1)
    []
    >>> perfect_functional(-222)
    []
    >>> perfect_functional("64")
    Traceback (most recent call last):
    ...
    List3_ex2_Dabrowski.ArgumentNotIntError
    """

    if type(n) != int:
        raise ArgumentNotIntError

    divisors = lambda x, c, l: l if c == 0 else (divisors(x, c - 1, l + [c]) if x % c == 0 else divisors(x, c - 1, l))
    list_sum = lambda a, l: a if not l else list_sum(a + l[0], l[1:])
    return list(filter(lambda x: list_sum(0, divisors(x, x - 1, [])) == x, range(2, n + 1)))


if __name__ == '__main__':
    # auto-documentation:
    # Docs\_build\html\index.html

    # testing
    doctest.testmod()

    # # Test 1:
    m = 800
    print(perfect_comprehension(m))
    print(perfect_imperative(m))
    print(perfect_functional(m))
    #
    # # Test 2 -> border case:
    # m = 1
    # print(perfect_comprehension(m))
    # print(perfect_imperative(m))
    # print(perfect_functional(m))
    #
    # # Test 3 -> weird input:
    # m = -222
    # print(perfect_comprehension(m))
    # print(perfect_imperative(m))
    # print(perfect_functional(m))
