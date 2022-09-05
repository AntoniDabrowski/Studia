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


def greedy_walking(M, positions, uncertainty_level):
    path = ""
    for _ in range(uncertainty_level):

        chosen_position = move("U",M,positions)
        chosen_move = "U"
        D_position = move("D",M,positions)
        if len(D_position) < len(chosen_position):
            chosen_position = D_position
            chosen_move = "D"

        L_position = move("L",M,positions)
        if len(L_position) < len(chosen_position):
            chosen_position = L_position
            chosen_move = "L"

        R_position = move("R",M,positions)
        if len(R_position) < len(chosen_position):
            chosen_position = R_position
            chosen_move = "R"

        path+=chosen_move
        positions = chosen_position
    return path, positions


def move(direction, M, positions):
    new_positions = set()
    if direction == "U":
        direction = np.array([0,-1])
    elif direction == "D":
        direction = np.array([0,1])
    elif direction == "L":
        direction = np.array([-1,0])
    elif direction == "R":
        direction = np.array([1,0])
    for element in positions:
        x, y = element+direction
        if M[y,x] == 0:
            new_positions.add((x,y))
        else:
            new_positions.add(element)
    return new_positions

def terminal_state(positiones,end):
    for position in positiones:
        if position not in end:
            return False
    return True


def BFS(M, positions, end):
    queue = [(positions,"")]
    checked = []
    while queue:
        current_positions, current_path = queue.pop(0)

        # print_map(M,current_positions,end)
        # sleep(1)
        # print(current_path,len(current_path),"\n")

        checked.append(current_positions)
        for direction in ["U","D","L","R"]:
            new_positions = move(direction,M,current_positions)
            new_path = current_path + direction
            if len(new_positions)<len(current_positions):
                queue=[(new_positions,new_path)]
                checked = []
                break

            if terminal_state(new_positions,end):
                return new_path

            if new_positions not in checked:
                queue.append((new_positions,new_path))

def find_path(map, uncertainty_level):
    M, positions, end = decode_map(map)
    path, positions = greedy_walking(M, positions, uncertainty_level)
    path += BFS(M, positions, end)
    return path


if __name__ == '__main__':
    map = """######################
                #SSSSSSSS#SSS##SSSSSS#
                #SSSSSSSSSSSS##SSSSSS#
                #SSSSSS###SSSSSSSSS#B#
                #SSSSSS###SSSSSSSSSSS#
                #SSSSSSSSSSSSSSSSSSSS#
                #####SSSSSSSSSSSSSSSS#
                #SSSSSSSSSSSSSSSSSSSS#
                ######################"""
    M, start, end = decode_map(map)
    # new_positions = move("D",M,start)
    # new_positions = greedy_walking(M,start,19)
    path = find_path(map,20)
    print(path)
    print(len(path))
    # print_map(M,new_positions,end)

