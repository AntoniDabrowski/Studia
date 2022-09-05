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

        if is_valid(partially_initialize_line, partial_sol):
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


def is_valid(sol_1, sol_2):
    for i in range(sol_1.shape[0]):
        if sol_1[i] != -1:
            if sol_1[i] != sol_2[i]:
                return False
    return True


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

# if __name__ == '__main__':
#     input = """        7 1
#         1 1 2
#         2 1 2
#         1 2 2
#         4 2 3
#         3 1 4
#         3 1 3
#         2 1 4
#         2 9
#         2 1 5
#         2 7
#         14
#         8 2
#         6 2 2
#         2 8 1 3
#         1 5 5 2
#         1 3 2 4 1
#         3 1 2 4 1
#         1 1 3 1 3
#         2 1 1 2
#         1 1 1 2
#         3 1 2 1 1
#         1 4 2 1 1
#         1 3 2 4
#         1 4 6 1
#         1 11 1
#         5 1 6 2
#         14
#         7 2
#         7 2
#         6 1 1
#         9 2
#         3 1 1 1
#         3 1 3
#         2 1 3
#         2 1 5
#         3 2 2
#         3 3 2
#         2 3 2
#         2 6"""
#     horizontal_constraints = []
#     vertical_constraints = []
#     x,y = 20,20
#     for i,line in enumerate(input.split("\n")):
#         l = []
#         for element in line.split():
#             l.append(int(element))
#         if i < x:
#             vertical_constraints.append(l)
#         else:
#             horizontal_constraints.append(l)
#     # print(len(veral_constraints))
#     # print(len(horizontal_constraints))
#     M = AC_3(horizontal_constraints, vertical_constraints)
#     print_nonogram(M)



# python validator.py zad1 python Z1.py