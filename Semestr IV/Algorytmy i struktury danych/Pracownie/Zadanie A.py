import numpy as np
import random
from tqdm.auto import tqdm


def example_generator(m):
    D = []
    N_d = []
    for i in range(m):
        D.append(random.randint(1, 10**9))
        N_d.append(random.randint(1, 10**9))
    return D, N_d


def alg1(D, N_d):
    d = {ds: nds for ds, nds in zip(D, N_d)}
    i = len(list(d.keys()))-1
    key = list(d.keys())[i]
    while np.sum(np.array(list(d.values())) > 1) > 0:
        if d.setdefault(key, 0) > 1:
            if 2 * key in d:
                d[2 * key] += 1
            else:
                d[2 * key] = 1
            d[key] -= 2
            if d[key] == 0:
                del d[key]
            key = max(d.keys())
            i = len(list(d.keys()))-1
        i -= 1
        key = list(d.keys())[i]
    return sum(d.values())


def alg2(D, N_d):
    d = {ds: nds for ds, nds in zip(D, N_d)}
    key = max(d.keys())
    while np.sum(np.array(list(d.values())) > 1) > 0:
        if d.setdefault(key, 0) > 1:
            if 2 * key in d:
                d[2 * key] += 1
            else:
                d[2 * key] = 1
            d[key] -= 2
            if d[key] == 0:
                del d[key]
        key = random.choice(list(d.keys()))
    return sum(d.values())


def cut(num):
    for i in range(1, len(num) + 1):
        if num[-i] == '1':
            return len(num) - i + 1


def my_alg(D, N_d):
    nums = {}
    for d, nd in tqdm(zip(D, N_d)):
        num_bin = bin(d)[2:]
        cutting_point = cut(num_bin)
        if num_bin[:cutting_point] in nums:
            nums[num_bin[:cutting_point]].append(bin(nd) + num_bin[cutting_point:])
        else:
            nums[num_bin[:cutting_point]] = [bin(nd) + num_bin[cutting_point:]]
    s = 0
    for key in nums.keys():
        s += bin(sum([int(num, 2) for num in nums[key]])).count('1')
    return s


if __name__ == "__main__":
    with open("Tests.txt", 'w', encoding='UTF-8') as output_file:
        for i in range(1):
            # m = np.random.randint(1,10**4)
            # m = 10**5
            # D, N_d = example_generator(m)
            m = (10**4)
            # D = [10**9]*m
            D = [10**9-i for i in range(m)]
            N_d = [10**9]*m
            # print(m)
            # print(D)
            # print(N_d)
            print(my_alg(D, N_d))
            # output_file.write(str(m)+"\n")
            # output_file.write(''.join(str(d)+", " for d in D)+"\n")
            # output_file.write(''.join(str(n_d)+", " for n_d in N_d)+"\n")
            # output_file.write(str(my_alg(D, N_d))+"\n")
