import numpy as np
from itertools import permutations
from queue import PriorityQueue


def calculate_position(starting_position, end_position):
    l = [0, 0]
    if end_position[0] < starting_position[0]:
        l[0] = 1
    elif end_position[0] > starting_position[0]:
        l[0] = -1

    if end_position[1] < starting_position[1]:
        l[1] = -1
    elif end_position[1] > starting_position[1]:
        l[1] = 1
    return tuple(l)

def path_length_normalization(sb, bspot):
    if 0 not in sb:
        if 0 not in bspot:
            if sb[0] != bspot[0] and sb[1] != bspot[1]:
                return 3, [(sb[0], 0), (0, sb[1])]
            else:
                if sb[0] != bspot[0]:
                    return 1, [(bspot[0] * (-1), 0)]
                if sb[1] != bspot[1]:
                    return 1, [(0, bspot[1] * (-1))]
                else:
                    return 1, [(bspot[0] * (-1), 0), (0, bspot[1] * (-1))]
        else:
            if sb[0] == bspot[0]:
                return -1, [(bspot[0] * (-1), 0)]
            elif sb[1] == bspot[1]:
                return -1, [(0, bspot[1] * (-1))]
            elif sb[0] == bspot[0] * (-1):
                return 1, [(bspot[0] * (-1), 0)]
            elif sb[1] == bspot[1] * (-1):
                return 1, [(0, bspot[1] * (-1))]
    else:
        if (bspot[0] == (-1) * sb[0] and bspot[0] != 0) or (bspot[1] == (-1) * sb[1] and bspot[1] != 0):
            return 3, [sb]
        elif bspot == sb:
            return -1, [(sb[0] * (-1), sb[1] * (-1))]
        else:
            if bspot[0] == sb[0] or bspot[0] == 0:
                return 1, [(0, bspot[1] * (-1))]
            else:
                return 1, [(bspot[0] * (-1), 0)]

def import_board(file_name):
    with open(file_name, 'r', encoding='UTF-8') as input_file:
        index = 0
        boxes = []
        spots = []
        first = True
        for line in input_file.read().split():
            l = np.zeros(len(line)).astype(int)
            for i, element in enumerate(line):
                if element == ".":
                    l[i] = 1
                elif element == "B":
                    boxes.append((index, i))
                    l[i] = 1
                elif element == "G":
                    l[i] = 2
                    spots.append((index, i))
                elif element == "*":
                    l[i] = 2
                    spots.append((index, i))
                    boxes.append((index, i))
                elif element == "+":
                    l[i] = 2
                    spots.append((index, i))
                    starting_position = (index, i)
                elif element == "K":
                    l[i] = 1
                    starting_position = (index, i)
            if first:
                partial_board = l.copy()
                first = False
            else:
                partial_board = np.vstack([partial_board, l])
            index += 1
    return partial_board, tuple(boxes), starting_position, spots


def legal_move(board, boxes, sokoban_position):
    x, y = sokoban_position
    legal_moves = []
    if board[x - 1, y] > 0:
        if (x - 1, y) not in boxes:
            legal_moves.append("U")
        elif board[x - 2, y] > 0 and (x - 2, y) not in boxes:
            legal_moves.append("U")
    if board[x + 1, y] > 0:
        if (x + 1, y) not in boxes:
            legal_moves.append("D")
        elif board[x + 2, y] > 0 and (x + 2, y) not in boxes:
            legal_moves.append("D")

    if board[x, y - 1] > 0:
        if (x, y - 1) not in boxes:
            legal_moves.append("L")
        elif board[x, y - 2] > 0 and (x, y - 2) not in boxes:
            legal_moves.append("L")

    if board[x, y + 1] > 0:
        if (x, y + 1) not in boxes:
            legal_moves.append("R")
        elif board[x, y + 2] > 0 and (x, y + 2) not in boxes:
            legal_moves.append("R")
    return legal_moves


def A_star(board, boxes, sokoban_position, spots):
    queue = PriorityQueue()
    queue.put((0, (sokoban_position, boxes, "")))
    visited_position = {(starting_position, boxes)}
    while queue:
        # print(visited_position,"\n\n")
        sokoban_position, boxes, path = queue.get()[1]
        legal_moves = legal_move(board, boxes, sokoban_position)
        for move in legal_moves:
            if move == "U":
                temp_sokoban_position = (sokoban_position[0] - 1, sokoban_position[1])
            elif move == "D":
                temp_sokoban_position = (sokoban_position[0] + 1, sokoban_position[1])
            elif move == "L":
                temp_sokoban_position = (sokoban_position[0], sokoban_position[1] - 1)
            elif move == "R":
                temp_sokoban_position = (sokoban_position[0], sokoban_position[1] + 1)
            temp_boxes = []
            for i in range(len(boxes)):
                if boxes[i] == temp_sokoban_position:
                    if move == "U":
                        temp_boxes.append((boxes[i][0] - 1, boxes[i][1]))
                    elif move == "D":
                        temp_boxes.append((boxes[i][0] + 1, boxes[i][1]))
                    elif move == "L":
                        temp_boxes.append((boxes[i][0], boxes[i][1] - 1))
                    elif move == "R":
                        temp_boxes.append((boxes[i][0], boxes[i][1] + 1))
                else:
                    temp_boxes.append(boxes[i])
            temp_boxes = tuple(temp_boxes)
            if (temp_sokoban_position, temp_boxes) not in visited_position:

                # Check if current position is winning
                winning_position = True
                for box in temp_boxes:
                    if board[box[0], box[1]] != 2:
                        winning_position = False
                        break
                if winning_position:
                    return path + move

                visited_position.add((temp_sokoban_position, temp_boxes))
                queue.put((len(path) + 1 + heuristic(temp_boxes, temp_sokoban_position, spots),
                              (temp_sokoban_position, temp_boxes, path + move)))


def heuristic(boxes, position, spots):
    m = np.inf
    for perm_boxes in permutations(boxes):
        for perm_spots in permutations(spots):
            temp_dist = [(position,0)]
            for spot, box in zip(perm_spots, perm_boxes):
                if box != spot:
                    update_temp_dist = []
                    for sokoban_position, dist in temp_dist:
                        num, l = path_length_normalization(calculate_position(sokoban_position,box),calculate_position(box,spot))
                        dist += np.abs(sokoban_position[0] - box[0]) + np.abs(sokoban_position[1] - box[1])
                        dist += np.abs(spot[0] - box[0]) + np.abs(spot[1] - box[1])
                        dist += num
                        for ending_position in l:
                            temp_sokoban_position = (spot[0]+ending_position[0],spot[1]+ending_position[1])
                            update_temp_dist.append((temp_sokoban_position,dist))
                    temp_dist = update_temp_dist
            m = min(m, min([el[1] for el in temp_dist]))
    return m


with open("zad_output.txt", 'w', encoding="UTF-8") as output_file:
    board, boxes, starting_position, spots = import_board("zad_input.txt")
    path = A_star(board, boxes, starting_position,spots)
    output_file.write(path + "\n")

# if __name__ == "__main__":
#     board, boxes, starting_position, spots = import_board("zad_input.txt")
#     path = A_star(board, boxes, starting_position,spots)
#     print(path)
#     print(len(path))

# python validator.py zad2 python Z2_A_star.py