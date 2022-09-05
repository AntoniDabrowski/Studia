import numpy as np


def test(a, b, n):
    if n < b:
        return True
    x_3 = n // b
    x_2 = (n - b * x_3) // a
    x_1 = n - b * x_3 - a * x_2
    alg_sol = x_1 + x_2 + x_3
    while x_3 != -1:
        x_2 = (n - b * x_3) // a
        x_1 = n - b * x_3 - a * x_2
        if x_1 + x_2 + x_3 < alg_sol:
            return False
        x_3 -= 1
    return True


def big_test(a, b, upper_bound):
    is_optimal = True
    for n in range(b, upper_bound):
        is_optimal = is_optimal and test(a, b, n)
    return is_optimal


def valid_pairs(upper_bound, lim=1000):
    M = np.zeros([upper_bound, upper_bound])
    for b in range(2, upper_bound):
        for a in range(2, b):
            M[b, a] = big_test(a, b, lim)

    return M


def hypothesis():
    M = np.zeros([1000, 1000]) # tablica wypełniona zerami
    for b in range(2, 1000): # większy nominał
        for a in range(2, b): # mniejszy nominał
            lower = (b / (a - 1)) - 1
            upper = (b - 1) / a
            ceil = np.ceil(lower)
            M[b, a] = ceil > upper
    return M


if __name__ == '__main__':
    M = hypothesis(100).astype(int)
    # M = (valid_pairs(100)).astype(int)
    print(M)
