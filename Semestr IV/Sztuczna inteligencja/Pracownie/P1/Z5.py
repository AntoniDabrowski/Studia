import numpy as np
from time import time, sleep


def print_nonogram(M):
    print(" " + "_" * M.shape[1])
    for line in M:
        s = "|"
        for element in line:
            if element == 0:
                s += ' '
            else:
                s += '1'
        s += "|"
        print(s)
    print(" " + "_" * M.shape[1])


def generate_pseudo_nonogram1(hight, width):
    M = np.zeros((hight, width)).astype(int)
    for line_index in range(hight):
        # print(int(width-np.abs(2*width/(hight-1) * line_index - width)+1))
        block_length = np.random.randint(0, int(width - np.abs(2 * width / (hight - 1) * line_index - width) + 1)) * 2
        while block_length > width:
            block_length -= 3
        # print(block_length)
        if block_length > 0:
            starting_point = np.random.randint(0, width - block_length + 1)
            M[line_index] = np.array(
                [0 if i < starting_point or i >= starting_point + block_length else 1 for i in range(width)])
    return M


def generate_pseudo_nonogram2(hight, width, covered_part=0.5):
    def generate_effective_set(M, filled_squares):
        effective_set = []
        for x, y in filled_squares:
            if (x - 1 >= 0 and M[x - 1, y] == 0) or (x + 1 < hight and M[x + 1, y] == 0) or (
                    y - 1 >= 0 and M[x, y - 1] == 0) or (y + 1 < width and M[x, y + 1] == 0):
                effective_set.append((x, y))
        return effective_set

    M = np.zeros((hight, width)).astype(int)
    x, y = np.random.randint(0, hight), np.random.randint(0, width)
    filled = [(x, y)]
    effective_set = [(x, y)]
    M[x, y] = 1
    while len(filled) < hight * width * covered_part:
        x, y = effective_set[np.random.randint(0, len(effective_set))]
        if np.random.randint(0, 2):
            x += np.abs(np.random.randint(0, 2) * 2) - 1
        else:
            y += np.abs(np.random.randint(0, 2) * 2) - 1
        if x >= 0 and x < hight and y >= 0 and y < width and M[x, y] == 0:
            if np.sum(M[:, y]) == 0 or np.sum(M[x, :]) == 0:
                filled.append((x, y))
                M[x, y] = 1
                effective_set = generate_effective_set(M, filled)
            elif ((x - 1 >= 0 and M[x - 1, y] == 1) and (y - 1 >= 0 and M[x, y - 1] == 1)) or \
                    ((x - 1 >= 0 and M[x - 1, y] == 1) and (y + 1 < width and M[x, y + 1] == 1)) or \
                    ((x + 1 < hight and M[x + 1, y] == 1) and (y - 1 >= 0 and M[x, y - 1] == 1)) or \
                    ((x + 1 < hight and M[x + 1, y] == 1) and (y + 1 < width and M[x, y + 1] == 1)):
                filled.append((x, y))
                M[x, y] = 1
                effective_set = generate_effective_set(M, filled)
    return M


def solution_to_riddle(M):
    #      horizontal_restriction,vertical_restriction
    return np.sum(M, axis=0), np.sum(M, axis=1)


def solved(M, horizontal_restriction, vertical_restriction):
    h, v = unsatisfied_restrictions(M, horizontal_restriction, vertical_restriction)
    if h or v:
        return False
    h, v = solution_to_riddle(M)
    comparison_one = h == horizontal_restriction
    comparison_two = v == vertical_restriction
    if comparison_one.all() and comparison_two.all():
        return True
    return False


def unsatisfied_restrictions(M, horizontal_restriction, vertical_restriction):
    unsatisfied_horizontal = set()
    for i in range(M.shape[0]):
        line = M[i, :]
        was_zero_after_one = False
        was_one = False
        for letter in line:
            if letter == 1 and was_zero_after_one:
                unsatisfied_horizontal.add(i)
            elif letter == 1:
                was_one = True
            elif letter == 0 and was_one:
                was_zero_after_one = True
        if np.sum(line) != horizontal_restriction[i]:
            unsatisfied_horizontal.add(i)

    unsatisfied_vertical = set()
    for i in range(M.shape[1]):
        line = M[:, i]
        was_zero_after_one = False
        was_one = False
        for letter in line:
            if letter == 1 and was_zero_after_one:
                unsatisfied_vertical.add(i)
            elif letter == 1:
                was_one = True
            elif letter == 0 and was_one:
                was_zero_after_one = True
        if np.sum(line) != vertical_restriction[i]:
            unsatisfied_vertical.add(i)

    return list(unsatisfied_horizontal), list(unsatisfied_vertical)


def opt_dist(L, D):
    m = np.Inf
    for i in range(len(L) - D + 1):
        Sol = np.array([1 if j >= i and j < i + D else 0 for j in range(len(L))])
        m = min(m, np.sum(np.logical_xor(L, Sol)))
    return m


def generate_initial_solution(horizontal_restriction, vertical_restriction):
    M = np.zeros((vertical_restriction.shape[0],horizontal_restriction.shape[0])).astype(int)
    for i in range(horizontal_restriction.shape[0]):
        if horizontal_restriction[i] > int(vertical_restriction.shape[0] / 2):
            M[:, i] = np.array([0 if index < vertical_restriction.shape[0] - horizontal_restriction[i] or
                                     horizontal_restriction[i] <= index else 1 for index in
                                range(vertical_restriction.shape[0])])
    for i in range(vertical_restriction.shape[0]):
        if vertical_restriction[i] > int(horizontal_restriction.shape[0] / 2):
            M[i, :] = np.logical_or(M[i, :], np.array([0 if index < horizontal_restriction.shape[0] -
                                                            vertical_restriction[i] or vertical_restriction[
                                                                i] <= index else 1 for index in
                                                       range(horizontal_restriction.shape[0])]))
    return M.T


def solve(horizontal_restriction, vertical_restriction, theta_0=0.1, theta_1=0.05, initial_solution='zeros'):
    hight, width = horizontal_restriction.shape[0], vertical_restriction.shape[0]
    if initial_solution == 'zeros':
        M = np.zeros((hight, width)).astype(int)
    elif initial_solution == 'smart':
        M = generate_initial_solution(horizontal_restriction, vertical_restriction)
        print_nonogram(M.T)

    dist = fitness_function(M, horizontal_restriction, vertical_restriction)
    id = 0
    while dist:
        unsatisfied_horizontal, unsatisfied_vertical = unsatisfied_restrictions(M, horizontal_restriction,
                                                                                vertical_restriction)
        id += 1
        r = np.random.random()

        # if dist<10:
        #     print(unsatisfied_horizontal)
        #     print(unsatisfied_vertical)
        #     if not unsatisfied_vertical and not unsatisfied_horizontal:
        #         print_nonogram(M.T)
        #         sleep(3)

        # optimal row+column fixing
        if r > theta_0:
            if (np.random.randint(0, 2) and unsatisfied_horizontal) or (
                    unsatisfied_horizontal and not unsatisfied_vertical):
                horizontal_index = np.random.choice(unsatisfied_horizontal)
                dist = np.Inf
                sol = None
                iterator = np.arange(width)
                np.random.shuffle(iterator)
                for i in iterator:
                    M[horizontal_index, i] = not M[horizontal_index, i]
                    temp_dist = fitness_function(M, horizontal_restriction, vertical_restriction)
                    if temp_dist < dist:
                        dist = temp_dist
                        sol = M.copy()
                    M[horizontal_index, i] = not M[horizontal_index, i]
                M = sol
            elif unsatisfied_vertical:
                vertical_index = np.random.choice(unsatisfied_vertical)
                dist = np.Inf
                sol = None
                iterator = np.arange(hight)
                np.random.shuffle(iterator)
                for i in iterator:
                    M[i, vertical_index] = not M[i, vertical_index]
                    temp_dist = fitness_function(M, horizontal_restriction, vertical_restriction)
                    if temp_dist < dist:
                        dist = temp_dist
                        sol = M.copy()
                    M[i, vertical_index] = not M[i, vertical_index]
                M = sol
        # optimal row/column fixing
        elif r > theta_1:
            if (np.random.randint(0, 2) and unsatisfied_horizontal) or (
                    unsatisfied_horizontal and not unsatisfied_vertical):
                horizontal_index = np.random.choice(unsatisfied_horizontal)
                dist = np.Inf
                sol = None
                iterator = np.arange(width)
                np.random.shuffle(iterator)
                for i in iterator:
                    M[horizontal_index, i] = not M[horizontal_index, i]
                    temp_dist = opt_dist(M[horizontal_index, :], horizontal_restriction[horizontal_index])
                    if temp_dist < dist:
                        dist = temp_dist
                        sol = M.copy()
                    M[horizontal_index, i] = not M[horizontal_index, i]
                M = sol
            elif unsatisfied_vertical:
                vertical_index = np.random.choice(unsatisfied_vertical)
                dist = np.Inf
                sol = None
                iterator = np.arange(hight)
                np.random.shuffle(iterator)
                for i in iterator:
                    M[i, vertical_index] = not M[i, vertical_index]
                    temp_dist = opt_dist(M[:, vertical_index], vertical_restriction[vertical_index])
                    if temp_dist < dist:
                        dist = temp_dist
                        sol = M.copy()
                    M[i, vertical_index] = not M[i, vertical_index]
                M = sol
        # random negation
        else:
            M[np.random.randint(0, hight), np.random.randint(0, width)] = not M[
                np.random.randint(0, hight), np.random.randint(0, width)]
        dist = fitness_function(M, horizontal_restriction, vertical_restriction)
        if id % 20 == 0:
            print(dist)
    return M.T


def fitness_function(M, horizontal_restriction, vertical_restriction):
    total_fitness = 0
    for i in range(M.shape[0]):
        line = M[i, :]
        total_fitness += opt_dist(line, horizontal_restriction[i])

    for i in range(M.shape[1]):
        line = M[:, i]
        total_fitness += opt_dist(line, vertical_restriction[i])
    return total_fitness


if __name__ == "__main__":
    # np.random.seed(2)
    M = generate_pseudo_nonogram2(15, 15)
    print("done")
    print_nonogram(M)
    horizontal_restriction, vertical_restriction = solution_to_riddle(M)
    print(horizontal_restriction)
    print(vertical_restriction)
    # M[2,2]=1
    # M[2,3]=1
    # print(fitness_function(M,horizontal_restriction,vertical_restriction))
    # print_nonogram(generate_initial_solution(horizontal_restriction, vertical_restriction))

    # t_0 = time()
    # print_nonogram(solve(horizontal_restriction, vertical_restriction,initial_solution='smart'))
    # # print_nonogram(solve(horizontal_restriction, vertical_restriction))
    # t_1 = time()
    # print(t_1 - t_0)
