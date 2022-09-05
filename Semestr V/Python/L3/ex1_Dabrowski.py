from numpy import linspace
from utils import plot_results


def prime_imperative(n):
    # input type: integer
    # output type: list of integers
    # specification: return list of primes less than or equal to n
    def is_prime(k):
        # input type: integer
        # output type: boolean
        # specification: Test whether n is prime
        if k < 2:
            return False
        for j in range(2, k):
            if k % j == 0:
                return False
        return True

    if n < 2:
        return []
    i = 2
    result = []
    while i <= n:
        if is_prime(i):
            result.append(i)
        i += 1
    return result


def prime_comprehension(n):
    # input type: integer
    # output type: list of integers
    # specification: return list of primes less than or equal to n
    return [i for i in range(2, n + 1) if i not in [x * y for x in range(2, n // 2 + 1) for y in range(2, n // 2 + 1)]]


def prime_functional(n):
    # input type: integer
    # output type: list of integers
    # specification: return list of primes less than or equal to n
    # p is a prime iff (p-1)!+1=0 (mod p)
    factorial_modulo = lambda x, p: 1 if x == 1 else (x * factorial_modulo(x - 1, p)) % p
    return list(filter(lambda x: (factorial_modulo(x - 1, x) + 1) % x == 0, range(2, n + 1)))


if __name__ == '__main__':
    # Test 1:
    m = 200
    print(prime_comprehension(m))
    print(prime_imperative(m))
    print(prime_functional(m))

    # Test 2 -> border case:
    m = 1
    print(prime_comprehension(m))
    print(prime_imperative(m))
    print(prime_functional(m))

    # Test 2 -> weird input:
    m = -101
    print(prime_comprehension(m))
    print(prime_imperative(m))
    print(prime_functional(m))

    # Time comparison:
    inputs = linspace(10, 300, 10, endpoint=True).astype(int)
    print("\nInputs for plot:\n", inputs)
    plot_results([prime_functional, prime_comprehension, prime_imperative],
                 ["functional", "comprehension", "imperative"], inputs, "Primes - time comparison")

    # Conclusion:
    # Function prime_imperative is the fastest, second place takes prime_functional and last prime_comprehension.
