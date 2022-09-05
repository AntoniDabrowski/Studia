import numpy as np
from itertools import combinations, product
from ordered_set import OrderedSet


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


def revise(line, constraint):
    partially_initialize_line = line.copy()
    known_elements = np.ones(partially_initialize_line.shape[0]).astype(bool)
    assumption = np.ones(partially_initialize_line.shape[0]).astype(int) * (-1)
    for i in range(assumption.shape[0]):
        const = partially_initialize_line.shape[0] - sum(constraint) + 1
        for combination in combinations(np.arange(const), len(constraint)):
            partial_sol = np.zeros(partially_initialize_line.shape[0]).astype(int)
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

            if is_valid(partially_initialize_line, partial_sol, constraint):
                for i in range(assumption.shape[0]):
                    if known_elements[i]:
                        if assumption[i] == -1:
                            assumption[i] = partial_sol[i]
                        elif assumption[i] != partial_sol[i]:
                            known_elements[i] = False
    for i in range(assumption.shape[0]):
        if known_elements[i] and partially_initialize_line[i] == -1:
            partially_initialize_line[i] = assumption[i]
    return partially_initialize_line


def is_valid(sol_1, sol_2, constraint):
    combined_sol = np.ones(sol_1.shape[0]).astype(int) * (-1)
    for i in range(sol_1.shape[0]):
        if sol_1[i] != -1:
            if sol_1[i] != sol_2[i]:
                return False
        combined_sol[i] = sol_2[i]

    new_constraint = []
    last_checked_is_zero = True
    for i in range(combined_sol.shape[0]):
        if combined_sol[i] == 1:
            if last_checked_is_zero:
                new_constraint.append(1)
                last_checked_is_zero = False
            else:
                new_constraint[-1] += 1
        else:
            last_checked_is_zero = True
    return constraint == new_constraint


def AC_3(horizontal_constraints, vertical_constraints):
    queue = OrderedSet(product(np.arange(len(horizontal_constraints)), [0])) | OrderedSet(
        product(np.arange(len(vertical_constraints)), [1]))
    M = np.ones([len(vertical_constraints), len(horizontal_constraints)]).astype(int) * (-1)
    while queue:
        index, axis = queue.pop()
        if axis == 0:
            line = M[:, index]
            new_line = revise(line, horizontal_constraints[index])
            for i in range(line.shape[0]):
                if line[i] != new_line[i] and new_line[i] != -1:
                    queue = OrderedSet([(i, 1)]) | queue
            M[:, index] = new_line
        if axis == 1:
            line = M[index, :]
            new_line = revise(line, vertical_constraints[index])
            for i in range(line.shape[0]):
                if line[i] != new_line[i] and new_line[i] != -1:
                    queue = OrderedSet([(i, 0)]) | queue
            M[index, :] = new_line
    return M


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

    M = AC_3(horizontal_constraints,vertical_constraints)
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

# python validator.py zad1 python Z1.py