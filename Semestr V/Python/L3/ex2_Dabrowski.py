from numpy import linspace
from utils import plot_results


def perfect_imperative(n):
    # input type: integer
    # output type: list of integers
    # specification: return list of perfect numbers less than or equal to n
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
    # input type: integer
    # output type: list of integers
    # specification: return list of perfect numbers less than or equal to n
    return [i for i in range(2, n + 1) if
            [a for a in [0] for j in [k for k in range(1, i) if i % k == 0] for a in [a + j]][-1] == i]


def perfect_functional(n):
    # input type: integer
    # output type: list of integers
    # specification: return list of perfect numbers less than or equal to n
    divisors = lambda x, c, l: l if c == 0 else (divisors(x, c - 1, l + [c]) if x % c == 0 else divisors(x, c - 1, l))
    list_sum = lambda a, l: a if not l else list_sum(a + l[0], l[1:])
    return list(filter(lambda x: list_sum(0, divisors(x, x - 1, [])) == x, range(2, n + 1)))


if __name__ == '__main__':
    # Test 1:
    m = 800
    print(perfect_comprehension(m))
    print(perfect_imperative(m))
    print(perfect_functional(m))

    # Test 2 -> border case:
    m = 1
    print(perfect_comprehension(m))
    print(perfect_imperative(m))
    print(perfect_functional(m))

    # Test 3 -> weird input:
    m = -222
    print(perfect_comprehension(m))
    print(perfect_imperative(m))
    print(perfect_functional(m))

    # Time comparison:
    # Experiment took about a minute on my computer
    inputs = linspace(20, 800, 15, endpoint=True).astype(int)
    print("\nInputs for plot:\n", inputs)
    plot_results([perfect_functional, perfect_comprehension, perfect_imperative],
                 ["funkcyjna", "składana", "imperatywna"], inputs, "Perfect numbers - time comparison")

    # Conclusion:
    # Function perfect_imperative is the mostly fastest, second place takes perfect_comprehension and
    # last perfect_functional.
