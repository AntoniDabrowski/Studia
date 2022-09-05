import numpy as np
from time import sleep
import random

def decode_map(list_of_strings):
    M = []
    start = set()
    end = []
    for y, l in enumerate(list_of_strings.split()):
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


def greedy_walking(M, positions, uncertainty_level=100,one=True):
    temp_positions = positions.copy()
    while len(temp_positions)>2:
        path = ""
        temp_positions = positions.copy()
        for _ in range(uncertainty_level):
            # print_map(M, positions, [])

            chosen_move = [(move("U", M, temp_positions),"U")]
            D_position = move("D", M, temp_positions)
            if len(D_position) < len(chosen_move[0][0]):
                chosen_move = [(D_position,"D")]
            elif len(D_position) == len(chosen_move[0][0]):
                chosen_move.append((D_position,"D"))

            L_position = move("L", M, temp_positions)
            if len(L_position) < len(chosen_move[0][0]):
                chosen_move = [(L_position, "L")]
            elif len(L_position) == len(chosen_move[0][0]):
                chosen_move.append((L_position, "L"))

            R_position = move("R", M, temp_positions)
            if len(R_position) < len(chosen_move[0][0]):
                chosen_move = [(R_position, "R")]
            elif len(R_position) == len(chosen_move[0][0]):
                chosen_move.append((R_position, "R"))

            # print(chosen_move)
            temp_positions, current_move = random.choice(chosen_move)
            path += current_move
            if len(temp_positions)<=2:
                break
            # print(current_move,"\n")
        # print_map(M, temp_positions, end)
        # print(path)
        # print("\n")
        # if one:
        #     break
    # print_map(M, temp_positions, [])
    # print("Done")
    return path, temp_positions


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


def BFS(M, positions, end,initial_depth):
    queue = [(positions, "")]
    checked = [positions]
    current_depth = 1
    first_marge = True
    while queue:
        current_positions, current_path = queue.pop(0)
        # if len(current_path)>current_depth:
        #     print("Queue len:",len(queue))
        #     current_depth=len(current_path)
        #     print(current_depth)
        if current_depth+initial_depth>150 or (first_marge and current_depth>=20):
            return "A"*150
        # print_map(M,current_positions,end)
        # sleep(1)
        # print(current_path,len(current_path),"\n")

        for direction in ["U", "D", "L", "R"]:
            new_positions = move(direction, M, current_positions)
            new_path = current_path + direction
            if len(new_positions) < len(current_positions):
                first_marge = False
                # print("Merged!")
                # print_map(M, new_positions, end)
                queue = [(new_positions, new_path)]
                checked = []
                break

            if terminal_state(new_positions, end):
                return new_path

            if new_positions not in checked:
                queue.append((new_positions, new_path))
            checked.append(new_positions)

def find_path(map, uncertainty_level):
    first = True
    while first or len(path)>150:
        M, positions, end = decode_map(map)
        path, positions = greedy_walking(M, positions, uncertainty_level)
        path += BFS(M, positions, end,len(path))
        first = False
    return path


# if __name__ == '__main__':
#     map = """        ######################
#         #SSSSSSSS#SSSSSSSSSBS#
#         #SSSSSSSSSSSS##SSSSSS#
#         #SSSSSSSS#############
#         #SSSSSS###SSSSSSSSSSS#
#         #SSSSSS###SSS#SSSSSSS#
#         #SSSSSSSS#SSS#SSSSSSS#
#         ##S#######SSS####SSSS#
#         #SSSSSSSSSSSSSSS#SSSS#
#         #SSSSSSSSSSSSSSS##SSS#
#         #SSSSSSSSSSSSSSSSSSSS#
#         #SSSS#################
#         #SSSSSSSSSSSSSSSSSSSS#
#         #SSSSSSSSSSSSSSSSSSSS#
#         #SSSSSSSSSSSSSSSSSSSS#
#         ######################"""
#
#     map2 = """        ######################
#         #SSSSSSSS#SSSSSSSSSBS#
#         #SSSSSSSSSSSS##SSSSSS#
#         #SSSSSSSS#############
#         #SSSSSS###SSSSSSSSSSS#
#         #SSSSSS###SSSSSSSSSSS#
#         #SSSSSSSS#SSSSSSSSSSS#
#         ##S#######SSSSSSSSSSS#
#         #SSSSSSSSSSSSSSSSSSSS#
#         #SSSSSSSSSSSSSSSSSSSS#
#         #SSSSSSSSSSSSSSSSSSSS#
#         #SSSSSSSSSSSSSSSSSSSS#
#         #SSSSSSSSSSSSSSSSSSSS#
#         #SSSSSSSSSSSSSSSSSSSS#
#         #SSSSSSSSSSSSSSSSSSSS#
#         ######################"""


    # M, start, end = decode_map(map2)
    # new_positions = move("D",M,start)
    # path, new_positions = greedy_walking(M, start, 100)
    # print(end)
    # print_map(M, start, end)
    # print("\n")
    # print_map(M, new_positions, end)
    # #
    # path = find_path(map2,90)
    # print(path)
    # print(len(path))

with open("zad_output.txt", 'w', encoding="UTF-8") as output_file, open("zad_input.txt", 'r', encoding='UTF-8') as input_file :
    map = ""
    for line in input_file.read().split():
        map += line
        map += "\n"
    path = find_path(map,100)
    output_file.write(path)

# python validator.py zad4 python Z4.py
