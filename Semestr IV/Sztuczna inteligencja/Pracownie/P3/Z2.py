import numpy as np
from itertools import combinations, product
from ordered_set import OrderedSet
from time import time


def print_nonogram(M):
    for line in M:
        s = ""
        for element in line:
            if element == 0:
                s += '.'
            elif element == 1:
                s += '#'
            else:
                s += " "
        print(s)


def is_valid(sol_1, sol_2):
    for i in range(sol_1.shape[0]):
        if sol_1[i] == 0 or sol_1[i] == 1:
            if sol_1[i] != sol_2[i]:
                return False
    return True


def revise(line, constraint):
    partially_initialize_line = line.copy()
    assumption = np.zeros(partially_initialize_line.shape[0])
    assumption_counter = 0

    const = partially_initialize_line.shape[0] - sum(constraint) + 1
    for combination in combinations(np.arange(const), len(constraint)):
        partial_sol = np.zeros(partially_initialize_line.shape[0])
        constraint_counter = 0
        combination_counter = 0
        for j in range(partially_initialize_line.shape[0]):
            if constraint_counter < len(constraint) and j >= combination[combination_counter] + sum(
                    constraint[:constraint_counter]):
                if j >= combination[combination_counter] + sum(constraint[:constraint_counter + 1]):
                    constraint_counter += 1
                    combination_counter += 1
                else:
                    partial_sol[j] = 1

        if is_valid(partially_initialize_line, partial_sol):
            assumption_counter += 1
            assumption += partial_sol
    if assumption_counter == 0:
        return assumption_counter, partially_initialize_line
    assumption = assumption / assumption_counter
    for i in range(assumption.shape[0]):
        if assumption[i] == 0 or assumption[i] == 1:
            partially_initialize_line[i] = assumption[i]
        else:
            # partially_initialize_line[i] = assumption[i]
            partially_initialize_line[i] = (partially_initialize_line[i]*1.6 + assumption[i]*0.4) / 2
    return assumption_counter, partially_initialize_line


def AC_3_initial(horizontal_constraints, vertical_constraints):
    queue = OrderedSet(product(np.arange(len(horizontal_constraints)), [0])) | OrderedSet(
        product(np.arange(len(vertical_constraints)), [1]))
    M = np.ones([len(vertical_constraints), len(horizontal_constraints)]) * 0.5
    while queue:
        index, axis = queue.pop()
        if axis == 0:
            line = M[:, index]
            _, new_line = revise(line, horizontal_constraints[index])
            for i in range(line.shape[0]):
                if line[i] != new_line[i] and (new_line[i] == 0 or new_line[i] == 1):
                    queue = OrderedSet([(i, 1)]) | queue
            M[:, index] = new_line
        if axis == 1:
            line = M[index, :]
            _, new_line = revise(line, vertical_constraints[index])
            for i in range(line.shape[0]):
                if line[i] != new_line[i] and (new_line[i] == 0 or new_line[i] == 1):
                    queue = OrderedSet([(i, 0)]) | queue
            M[index, :] = new_line
    return M


# def to_check(M):
#     rows = [(i, 0) for i in range(M.shape[0]) if not (np.logical_or(M[i] == 1, M[i] == 0)).all()]
#     columns = [(i, 1) for i in range(M.shape[1]) if not (np.logical_or(M[:, i] == 1, M[:, i] == 0)).all()]
#     return rows + columns


def AC_3(horizontal_constraints, vertical_constraints, M_new, changed_row, changed_column):
    M=M_new.copy()
    queue = OrderedSet([(changed_row, 0), (changed_column, 1)])
    while queue:
        index, axis = queue.pop()
        if axis == 0:
            line = M[:, index]
            assumption_counter, new_line = revise(line, horizontal_constraints[index])
            if assumption_counter == 0:
                return False, M
            for i in range(line.shape[0]):
                if line[i] != new_line[i] and (new_line[i] == 0 or new_line[i] == 1):
                    queue = OrderedSet([(i, 1)]) | queue
            M[:, index] = new_line
        if axis == 1:
            line = M[index, :]
            assumption_counter, new_line = revise(line, vertical_constraints[index])
            if assumption_counter == 0:
                return False, M
            for i in range(line.shape[0]):
                if line[i] != new_line[i] and (new_line[i] == 0 or new_line[i] == 1):
                    queue = OrderedSet([(i, 0)]) | queue
            M[index, :] = new_line
    return True, M


def select_variable_and_value(M, close_to, join=True):
    l = []
    for y in range(M.shape[0]):
        for x in range(M.shape[1]):
            if M[y, x] != 0 and M[y, x] != 1:
                l.append((y, x, abs(M[y, x] - close_to)))
    y, x, z = min(l, key=lambda t: t[2])

    if z < 0.5:
        if join:
            value = round(close_to)
        else:
            value = 1 - round(close_to)
    else:
        if join:
            value = 1 - round(close_to)
        else:
            value = round(close_to)
    return y, x, value


def select_variable_and_value2(M, close_to, join=True):
    l = []
    for y in range(M.shape[0]):
        for x in range(M.shape[1]):
            if M[y, x] != 0 and M[y, x] != 1:
                l.append((y, x, min(M[y, x],abs(M[y, x] - 1))))
    y, x, _ = min(l, key=lambda t: t[2])
    value = round(M[y,x])
    return y, x, value

def constraints(M):
    horizontal_constraints = []
    vertical_constraints = []
    for x in range(M.shape[0]):
        last_zero = True
        l = []
        for y in range(M.shape[1]):
            if M[x, y] == 1:
                if last_zero:
                    l.append(1)
                    last_zero = False
                else:
                    l[-1] += 1
            else:
                last_zero = True

        vertical_constraints.append(l)

    for y in range(M.shape[1]):
        last_zero = True
        l = []
        for x in range(M.shape[0]):
            if M[x, y] == 1:
                if last_zero:
                    l.append(1)
                    last_zero = False
                else:
                    l[-1] += 1
            else:
                last_zero = True
        horizontal_constraints.append(l)
    return horizontal_constraints, vertical_constraints


def backtrack(M, horizontal_constraints, vertical_constraints, close_to, join, depth):
    # print(depth,np.sum(np.logical_or(M == 0, M == 1)) / (0.01 * len(horizontal_constraints) * len(vertical_constraints)))
    # if depth%10==0:
    #     print_nonogram(M)
    if np.sum(np.logical_or(M == 0, M == 1)) == len(horizontal_constraints) * len(vertical_constraints):
        if (horizontal_constraints, vertical_constraints) == constraints(M):
            return True, M
        return False, M
    y, x, value = select_variable_and_value(M, close_to, join)
    for val in [value, 1 - value]:
        M[y, x] = val
        success_AC_3, M_AC_3 = AC_3(horizontal_constraints, vertical_constraints, M, x, y)
        if success_AC_3:
            success_backtrack, M_backtrack = backtrack(M_AC_3, horizontal_constraints, vertical_constraints, close_to,
                                                       join, depth + 1)
            if success_backtrack:
                return True, M_backtrack
    return False, M


with open("zad_input.txt", 'r', encoding='UTF-8') as input_file, open("zad_output.txt", 'w',
                                                                      encoding="UTF-8") as output_file:
    first_line = input_file.readline().split()
    x,y = int(first_line[0]), int(first_line[1])
    horizontal_constraints = []
    vertical_constraints = []
    for i in range(x):
        l = [int(element) for element in input_file.readline().split()]
        vertical_constraints.append(l)

    for i in range(y):
        l = [int(element) for element in input_file.readline().split()]
        horizontal_constraints.append(l)

    close_to = 1
    join = False
    M = AC_3_initial(horizontal_constraints, vertical_constraints)
    # print_nonogram(M)
    is_good, M = backtrack(M, horizontal_constraints, vertical_constraints, close_to, join, 0)
    # print_nonogram(M)

    for line in M:
        s = ""
        for element in line:
            if element == 0:
                s += '.'
            elif element == 1:
                s += '#'
            else:
                s += " "
        output_file.write(s + "\n")

# if __name__ == '__main__':
#     input = """1 1 2 2
#         5 5 7
#         5 2 2 9
#         3 2 3 9
#         1 1 3 2 7
#         3 1 5
#         7 1 1 1 3
#         1 2 1 1 2 1
#         4 2 4
#         1 2 2 2
#         4 6 2
#         1 2 2 1
#         3 3 2 1
#         4 1 15
#         1 1 1 3 1 1
#         2 1 1 2 2 3
#         1 4 4 1
#         1 4 3 2
#         1 1 2 2
#         7 2 3 1 1
#         2 1 1 1 5
#         1 2 5
#         1 1 1 3
#         4 2 1
#         3
#         2 2 3
#         4 1 1 1 4
#         4 1 2 1 1
#         4 1 1 1 1 1 1
#         2 1 1 2 3 5
#         1 1 1 1 2 1
#         3 1 5 1 2
#         3 2 2 1 2 2
#         2 1 4 1 1 1 1
#         2 2 1 2 1 2
#         1 1 1 3 2 3
#         1 1 2 7 3
#         1 2 2 1 5
#         3 2 2 1 2
#         3 2 1 2
#         5 1 2
#         2 2 1 2
#         4 2 1 2
#         6 2 3 2
#         7 4 3 2
#         7 4 4
#         7 1 4
#         6 1 4
#         4 2 2
#         2 1"""
#     input = """3
#         1 2
#         1 4
#         1 1 2
#         1 1 1 1
#         1 3 2
#         2 3 1
#         1 1 1 2
#         2 2 2
#         1 1 2 2
#         1 1 2 2
#         1 1 1 1
#         4 1 1
#         2 2 2 1
#         2 3 3
#         2 2 3
#         1 3 1 1
#         2 1 1 1 2
#         1 2 3
#         1 6
#         4 3
#         6 1 2 3
#         2 3
#         6
#         1 2 2
#         1 1 2
#         2 4 1 1
#         1 1 2 2 2 1
#         1 1 1 2 1 1
#         1 3 2 3
#         3 2 2
#         4 3 4 2
#         1 3 4 5
#         2 2
#         3"""
#
#     horizontal_constraints = []
#     vertical_constraints = []
#     x, y = 20, 15
#     for i, line in enumerate(input.split("\n")):
#         l = []
#         for element in line.split():
#             l.append(int(element))
#         if i < x:
#             vertical_constraints.append(l)
#         else:
#             horizontal_constraints.append(l)
#     # print(vertical_constraints)
#     # print(horizontal_constraints)
#     close_to = 1
#     join = False
#     t_0 = time()
#     M = AC_3_initial(horizontal_constraints, vertical_constraints)
#     # print_nonogram(M)
#     # print("----------------------------")
#     t_1 = time()
#     # print(t_1-t_0)
#     is_good, M = backtrack(M, horizontal_constraints, vertical_constraints, close_to, join, 0)
#     t_2 = time()
#     # print_nonogram(M)
#     print(is_good)
#     print(t_2-t_1)
#     # print(repr(M))


# python validator.py zad2 python Z2.py
