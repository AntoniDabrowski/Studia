import numpy as np
from tqdm.auto import tqdm
from itertools import chain, combinations
from numpy.linalg import matrix_power
from time import time


def convert_to_tuple(arr):
    l = list(arr[:, 0]) + list(arr[:, 1])
    return tuple(l)


def powerset():
    s = list(range(5))
    l = []
    for element in list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))):
        column = np.zeros((5, 1)).astype(int)
        for j in element:
            column[j, 0] = 1
        l.append(column)
    return l


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
    # return list of boolean matrices


def convert_from_tuple(arr):
    m = []
    for j in range(2):
        l = []
        for i in range(5):
            l.append(arr[5 * j + i])
        m.append(l)
    return np.array(m).T


def calculate_first_stage(restrictions):
    d = dict()
    total_sum = 0
    for first_col in powerset():
        for second_col in powerset():
            for third_col in powerset():
                m = np.hstack([first_col, second_col, third_col])
                is_good = 1
                for restriction in restrictions:
                    if (restriction == m[:3, :]).all() or (restriction == m[1:4, :]).all() or (
                            restriction == m[2:5, :]).all():
                        is_good = 0
                        break
                total_sum += is_good

                if is_good:
                    n = np.hstack([second_col, third_col])
                    for restriction in restrictions:
                        if (restriction[:, :2] == n[:3, :]).all() or (restriction[:, :2] == n[1:4, :]).all() or (
                                restriction[:, :2] == n[2:5, :]).all():
                            converted = convert_to_tuple(n)
                            if converted in d:
                                d[converted] += 1
                            else:
                                d[converted] = 1
                            break
    return d, total_sum

    # returns:
    #   dict with potentially bad ending as key and number of combinations leading to this ending as value
    #   total sum


def check4(restrictions, m):
    # restrictions = convert_restrictions(restrictions)
    total_sum = 0
    for first_col in tqdm(powerset()):
        for second_col in powerset():
            for third_col in powerset():
                for fourth_col in powerset():
                    m1 = np.hstack([first_col, second_col, third_col])
                    m2 = np.hstack([second_col, third_col, fourth_col])
                    is_good = 1
                    for restriction in restrictions:
                        if (restriction == m1[:3, :]).all() or (restriction == m1[1:4, :]).all() or (
                                restriction == m1[2:5, :]).all():
                            is_good = 0
                            break
                        if (restriction == m2[:3, :]).all() or (restriction == m2[1:4, :]).all() or (
                                restriction == m2[2:5, :]).all():
                            is_good = 0
                            break
                    total_sum += is_good
    return total_sum % m


def check5(restrictions, m):
    restrictions = convert_restrictions(restrictions)
    total_sum = 0
    for first_col in tqdm(powerset()):
        for second_col in powerset():
            for third_col in powerset():
                for fourth_col in powerset():
                    for fifth_col in powerset():
                        m1 = np.hstack([first_col, second_col, third_col])
                        m2 = np.hstack([second_col, third_col, fourth_col])
                        m3 = np.hstack([third_col, fourth_col, fifth_col])
                        is_good = 1
                        for restriction in restrictions:
                            if (restriction == m1[:3, :]).all() or (restriction == m1[1:4, :]).all() or (
                                    restriction == m1[2:5, :]).all():
                                is_good = 0
                                break
                            if (restriction == m2[:3, :]).all() or (restriction == m2[1:4, :]).all() or (
                                    restriction == m2[2:5, :]).all():
                                is_good = 0
                                break
                            if (restriction == m3[:3, :]).all() or (restriction == m3[1:4, :]).all() or (
                                    restriction == m3[2:5, :]).all():
                                is_good = 0
                                break
                        total_sum += is_good
    return total_sum % m


def calculate_line(restrictions, n, m):
    restrictions = convert_restrictions(restrictions)
    d, total_sum = calculate_first_stage(restrictions)

    for i in range(n - 3):
        new_d = dict()
        current_total_sum = 0
        for third_col in powerset():
            current_sum = total_sum
            for first_second_col in d.keys():
                first_second_col = convert_from_tuple(first_second_col)
                merged = np.hstack([first_second_col, third_col])
                is_good = True
                for restriction in restrictions:
                    if (restriction == merged[:3, :]).all() or (restriction == merged[1:4, :]).all() or (
                            restriction == merged[2:5, :]).all():
                        current_sum -= d[convert_to_tuple(first_second_col)]
                        is_good = False
                        break
                if is_good:
                    # updating dict
                    n = merged[:, 1:]
                    for restriction in restrictions:
                        if (restriction[:, :2] == n[:3, :]).all() or (restriction[:, :2] == n[1:4, :]).all() or (
                                restriction[:, :2] == n[2:5, :]).all():
                            converted_end = convert_to_tuple(n)
                            if converted_end in new_d:
                                new_d[converted_end] += d[convert_to_tuple(first_second_col)]
                            else:
                                new_d[converted_end] = d[convert_to_tuple(first_second_col)]
                            break
            # print(current_sum)
            current_total_sum += current_sum
        d = new_d
        return d
        total_sum = current_total_sum
    return total_sum % m


# returns:
#   updated dict of endings
#   total sum


def convert_to_num(arr):
    num = '0b' + ''.join([str(element) for line in arr.T for element in line])
    return int(num, 2)


def is_good(m, restrictions):
    for restriction in restrictions:
        if (restriction == m[:3, :]).all() or (restriction == m[1:4, :]).all() or (
                restriction == m[2:5, :]).all():
            return False
    return True


def initial_state(restrictions):
    M = np.zeros((1024, 1024)).astype(int)
    Num = np.zeros(1024).astype(int)
    for column_one in powerset():
        for column_two in powerset():
            for column_three in powerset():
                if is_good(np.hstack([column_one, column_two, column_three]), restrictions):
                    Num[convert_to_num(np.hstack([column_two, column_three]))] += 1
                    M[convert_to_num(np.hstack([column_two, column_three])), convert_to_num(
                        np.hstack([column_one, column_two]))] = 1
    return M, Num

def fast_matrix_mod_exp(M,n,m):
    W = np.identity(M.shape[0]).astype(int)
    if n==0:
        return W
    while n>1:
        print(n)
        if n % 2 == 1:
            W = np.matmul(M,W) % m
        M = np.matmul(M,M) % m
        n = n // 2
    return np.matmul(W,M) % m

def alg(num, M, n, m):
    M = fast_matrix_mod_exp(M,n-3,m)
    num = np.matmul(M, num)
    return np.sum(num) % m


if __name__ == "__main__":
    restrictions = """x..
..x
.x.
...
xxx
...
"""
    new = []
    for i,l in enumerate(restrictions.split()):
        if i%3==0:
            if i!=0:
                new.append(restriction[:-1])
            restriction = ""
        restriction+=l+"\n"
    new.append(restriction[:-1])
    restrictions = new
    # restrictions = ["""###
    #                    #..
    #                    .##""",
    #                 """..#
    #                    .#.
    #                    #.."""]

    # restrictions = ["""...
    #                    ...
    #                    ..."""]
    # # # #
    # restrictions = [""".##
    #                    #..
    #                    .##"""]


    restrictions = convert_restrictions(restrictions)
    # restrictions = [np.random.randint(0,2,(3,3)).astype(int) for _ in range(np.random.randint(2,5))]
    # for restriction in restrictions:
    #     print(restriction)

    m = 1000000
    n = 3
    M, Num = initial_state(restrictions)
    # # for n in Num:
    # #     print(n)
    print(np.sum(Num)%m)
    # t_0 = time()
    print(alg(Num,M,n,m)) # 693746
    # t_1 = time()
    # print(t_1-t_0)
    # total_sum = check4(restrictions,m)
    # print(total_sum)

    # restrictions = ["""...
    #                    ...
    #                    ..."""]
    #
    # restrictions = [""".##
    #                    #..
    #                    .##"""]

    # m = 1000000
    #
    # d = calculate_line(restrictions, 5, m)
    # # print(total_sum)
    #
    # for key in d.keys():
    #     print(convert_from_tuple(key),d[key])
    # print(len(d.keys()))
    # print("\n\n")
    #
    # restrictions = convert_restrictions(restrictions)
    # d, total_sum = calculate_first_stage(restrictions)
    #
    # for key in d.keys():
    #     print(convert_from_tuple(key),d[key])
    # print(len(d.keys()))
    # print("\n\n")

    # total_sum = calculate_line(restrictions,5,m)
    # print(total_sum)

    # total_sum = check4(restrictions,m)
    # print(total_sum)
