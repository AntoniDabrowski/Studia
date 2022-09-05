import numpy as np
from ordered_set import OrderedSet



def import_board(file_name):
    with open(file_name, 'r', encoding='UTF-8') as input_file:
        index = 0
        boxes = []
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
                elif element == "*":
                    l[i] = 2
                    boxes.append((index, i))
                elif element == "+":
                    l[i] = 2
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
    return partial_board, tuple(boxes), starting_position


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


def BFS(board, boxes, sokoban_position):
    queue = [(sokoban_position, boxes, "")]
    visited_position = {(starting_position, boxes)}
    while queue:
        sokoban_position, boxes, path = queue.pop(0)
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
                queue.append((temp_sokoban_position, temp_boxes, path + move))


with open("zad_output.txt", 'w', encoding="UTF-8") as output_file:
    board, boxes, starting_position = import_board("zad_input.txt")
    path = BFS(board, boxes, starting_position)
    output_file.write(path + "\n")

# python validator.py zad2 python Z2.py
