import numpy as np


def convert_restrictions(restrictions):
    l = []
    for restriction in restrictions:
        m = np.zeros((3, 3)).astype(int)
        for y, line in enumerate(restriction.split()):
            m[y, 0] = line[0] == 'x' or line[0] == '#'
            m[y, 1] = line[1] == 'x' or line[1] == '#'
            m[y, 2] = line[2] == 'x' or line[2] == '#'
        l.append(m)
    return l


def convert_to_num(restrictions):
    new = np.zeros(len(restrictions)).astype(int)
    for restriction in restrictions:
        for x in range(3):
            for y in range(3):
                new += restriction[x, y] * np.power(2, x + 5 * y)
    return new


def is_good(i, restrictions):
    for restriction in restrictions:
        if (i % 8 + (i % pow(2, 8) - i % pow(2, 5)) * pow(2, 5) + (i % pow(2, 13) - i % pow(2, 10)) * pow(2,
                                                                                                          10)) == restriction or (
                (i % pow(2, 4) - i % 2) + (i % pow(2, 9) - i % pow(2, 6)) * pow(2, 5) + (
                i % pow(2, 14) - i % pow(2, 11)) * pow(2, 10)) == restriction or (
                (i % pow(2, 5) - i % 4) + (i % pow(2, 10) - i % pow(2, 7)) * pow(2, 5) + (i - i % pow(2, 12)) * pow(2,
                                                                                                                    10)) == restriction:
            return False
    return True


def initialize(restrictions):
    num = np.zeros(1024).astype(int)
    adjacency_vec = np.zeros(1024).astype(int)
    for i in range(np.power(2, 15)):
        if is_good(i, restrictions):
            pass


if __name__ == "__main__":
    restrictions = ["""x..\n...\n..."""]
    restrictions = convert_restrictions(restrictions)
    restrictions = convert_to_num(restrictions)
    print(is_good(2, restrictions))
