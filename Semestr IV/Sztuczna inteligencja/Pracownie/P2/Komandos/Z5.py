import numpy as np
from time import sleep, time
import random
from queue import PriorityQueue
from itertools import permutations


def decode_map(list_of_strings):
    M = []
    start = set()
    end = []
    for y, l in enumerate(list_of_strings):
        current_row = []
        for x, element in enumerate(l):
            if element == " ":
                current_row.append(0)
            elif element == "#":
                current_row.append(1)
            elif element == "G":
                end.append((x, y))
                current_row.append(0)
            elif element == "S":
                start.add((x, y))
                current_row.append(0)
            elif element == "B":
                start.add((x, y))
                end.append((x, y))
                current_row.append(0)
        M.append(current_row)
    return np.array(M), start, end


def print_map(M, positions, end):
    for y, line in enumerate(M):
        current_row = ""
        for x, element in enumerate(line):
            if element == 1:
                current_row += "#"
            elif (x, y) in positions and (x, y) in end:
                current_row += "B"
            elif (x, y) in positions:
                current_row += "S"
            elif (x, y) in end:
                current_row += "G"
            else:
                current_row += " "
        print(current_row)


def move(direction, M, positions):
    new_positions = set()
    if direction == "U":
        direction = np.array([0, -1])
    elif direction == "D":
        direction = np.array([0, 1])
    elif direction == "L":
        direction = np.array([-1, 0])
    elif direction == "R":
        direction = np.array([1, 0])
    for element in positions:
        x, y = element + direction
        if M[y, x] == 0:
            new_positions.add((x, y))
        else:
            new_positions.add(element)
    return new_positions


def terminal_state(positions, end):
    for position in positions:
        if position not in end:
            return False
    return True


def A_star(M, positions, end):
    # print("\n")
    queue = PriorityQueue()
    queue.put((0, (positions, "")))
    checked = [positions]
    while queue:
        current_positions, current_path = queue.get()[1]

        # if len(current_path)>current_depth:
        #     print("Queue len:",len(queue))
        #     current_depth=len(current_path)
        #     print(current_depth)

        for direction in ["U", "D", "L", "R"]:
            new_positions = move(direction, M, current_positions)
            new_path = current_path + direction

            if terminal_state(new_positions, end):
                return new_path

            current_path_length = len(new_path)
            if new_positions not in checked:
                # print(current_path_length + heuristics(new_positions, end), (new_positions, new_path))
                queue.put((current_path_length + heuristics(M, new_positions, end), (new_positions, new_path)))
                checked.append(new_positions)
            # if current_path_length in checked:
            #     checked[current_path_length].append(new_positions)
            # else:
            #     checked[current_path_length] = [new_positions]


def crop_ends(positions, ends):
    new_ends = set()
    for end in ends:
        if end not in positions:
            new_ends.add(end)
    return new_ends


def BFS(M, positions, end):
    solutions = dict()
    queue = [(positions, 0)]
    checked = [positions]
    while queue and len(solutions) < len(end):
        current_positions, current_depth = queue.pop(0)

        for direction in ["U", "D", "L", "R"]:
            new_positions = move(direction, M, current_positions)

            for end_position in end:
                if end_position in new_positions:
                    if end_position in solutions:
                        solutions[end_position] = min(solutions[end_position], current_depth + 1)
                    else:
                        solutions[end_position] = current_depth + 1

            if new_positions not in checked:
                queue.append((new_positions, current_depth + 1))
            checked.append(new_positions)
    return max(solutions.values())


def heuristics(M, positions, end):
    result = BFS(M, end, positions)
    return result

    # + (1 - 1 / len(positions))


def heuristics2(M, positions, end):
    result = 0
    # print(positions)
    # print(end)
    for x, y in positions:
        for x_end, y_end in end:
            result = max(result, abs(x_end - x) + abs(y_end - y))
    return result


if __name__ == '__main__':
    map = """#####
#G  #
#   #
#  G#
#S# #
#   #
#SSS#
#####"""

    map2 = """######################
#        #   ##S     #
#            ##      #
#      ###         #G#
#S     ###           #
#                    #
#####         S      #
# S                  #
######################"""

    map3 = """######################
#        #         G #
#            ##      #
#       S#############
#      ###           #
#      ###           #
#        #           #
## #######           #
#   S                #
#                    #
#                    #
#                    #
#                    #
#                    #
#                  S #
######################"""

    M, start, end = decode_map(map3.split("\n"))

    print_map(M, start, end)
    for _ in range(1000):
        heuristics(M, start, end)
    # t_0 = time()
    # path = A_star(M,start,end)
    # t_1 = time()
    # print(path,len(path))

# with open("zad_output.txt", 'w', encoding="UTF-8") as output_file, open("zad_input.txt", 'r',
#                                                                         encoding='UTF-8') as input_file:
#     map = []
#
#     current_line = ""
#     for letter in input_file.read():
#         if letter!="\n":
#             current_line+=letter
#         else:
#             map.append(current_line)
#             current_line=""
#
#     M, start, end = decode_map(map)
#     # print_map(M,start,end)
#     path = A_star(M,start,end)
#     output_file.write(path)

# python validator.py zad5 python Z5.py
