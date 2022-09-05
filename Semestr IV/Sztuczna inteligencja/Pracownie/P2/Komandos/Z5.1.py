import numpy as np
from time import sleep, time
import random
from queue import PriorityQueue
from itertools import permutations


def decode_map(list_of_strings):
    M = []
    start = set()
    end = []
    all_positions = []
    for y, l in enumerate(list_of_strings):
        current_row = []
        for x, element in enumerate(l):
            if element == " ":
                current_row.append(0)
                all_positions.append((x, y))
            elif element == "#":
                current_row.append(1)
            elif element == "G":
                end.append((x, y))
                all_positions.append((x, y))
                current_row.append(0)
            elif element == "S":
                start.add((x, y))
                all_positions.append((x, y))
                current_row.append(0)
            elif element == "B":
                start.add((x, y))
                end.append((x, y))
                all_positions.append((x, y))
                current_row.append(0)
        M.append(current_row)
    return np.array(M), start, end, all_positions


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


def A_star(M, positions, end,d):
    # print("\n")
    queue = PriorityQueue()
    queue.put((0, (positions, "")))
    checked = [positions]
    founded = ""
    
    while queue:
        val,p = queue.get()
        current_positions, current_path = p
        # print(val, founded)
        if founded:
            if val>=len(founded):
                return founded
        # if len(current_path)>current_depth:
        #     print("Queue len:",len(queue))
        #     current_depth=len(current_path)
        #     print(current_depth)

        for direction in ["U", "D", "L", "R"]:
            new_positions = move(direction, M, current_positions)
            new_path = current_path + direction

            if terminal_state(new_positions, end):
                if not founded:
                    founded = new_path
                else:
                    if len(new_path) < len(founded):
                        founded = new_path

            current_path_length = len(new_path)
            if new_positions not in checked:
                # print(current_path_length + heuristics(new_positions, end), (new_positions, new_path))
                queue.put((current_path_length + heuristics(new_positions,d), (new_positions, new_path)))
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
    solutions = {end: 0}
    queue = [(end, 0)]
    checked = [end]
    while queue and len(solutions) < len(positions):
        current_position, current_depth = queue.pop(0)

        for direction in ["U", "D", "L", "R"]:
            new_position = list(move(direction, M, [current_position]))[0]

            if new_position not in checked:
                if new_position not in solutions:
                    solutions[new_position] = current_depth + 1
                queue.append((new_position, current_depth + 1))
                checked.append(new_position)
    return solutions


def heuristics(positions, d):
    result = 0
    for position in positions:
        result = max(result,d[position])
    return result



def heuristics2(M, positions, end):
    result = 0
    # print(positions)
    # print(end)
    for x, y in positions:
        for x_end, y_end in end:
            result = max(result, abs(x_end - x) + abs(y_end - y))
    return result

def preprocessing(M, all_positions, end):
    d = BFS(M, all_positions, end[0])
    if len(end)>1:
        for current_end in end[1:]:
            d_temp = BFS(M, all_positions, current_end)
        for key in d:
            d[key] = min(d[key],d_temp[key])
    return d

# if __name__ == '__main__':
#     map = """#####
# #G  #
# #   #
# #  G#
# #S# #
# #   #
# #SSS#
# #####"""
#
#     map2 = """######################
# #        #   ##S     #
# #            ##      #
# #      ###         #G#
# #S     ###           #
# #                    #
# #####         S      #
# # S                  #
# ######################"""
#
#     map3 = """######################
# #        #   ##S     #
# # S          ##      #
# #    S ###         #G#
# #      ###           #
# #                    #
# #####        SS      #
# #S                   #
# ######################"""
#
#     M, start, end, all_positions = decode_map(map3.split("\n"))
#     d = preprocessing(M,all_positions,end)
#     # print(heuristics(list(start),d))
#     # print(d)
#     t_0 = time()
#     path = A_star(M,start,end,d)
#     t_1 = time()
#     print(path,len(path))

with open("zad_output.txt", 'w', encoding="UTF-8") as output_file, open("zad_input.txt", 'r',
                                                                        encoding='UTF-8') as input_file:
    map = []

    current_line = ""
    for letter in input_file.read():
        if letter!="\n":
            current_line+=letter
        else:
            map.append(current_line)
            current_line=""

    M, start, end, all_positions = decode_map(map)
    d = preprocessing(M,all_positions,end)
    path = A_star(M,start,end,d)

    output_file.write(path)

# python validator.py zad5 python Z5.1.py
