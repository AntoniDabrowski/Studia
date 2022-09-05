import numpy as np
import random

def import_crossword_shape(lines):
    dict_of_words = dict()
    board_horizontal = np.ones((len(lines), len(lines[0]))).astype(int) * (-1)
    board_vertical = np.ones((len(lines), len(lines[0]))).astype(int) * (-1)
    position_horizontal = np.ones((len(lines), len(lines[0]))).astype(int) * (-1)
    position_vertical = np.ones((len(lines), len(lines[0]))).astype(int) * (-1)
    current_id = 0
    for y, line in enumerate(lines):
        last_signe_was_hash = False
        for x, sign in enumerate(line):
            if (x == 0 and sign == '#') or (not last_signe_was_hash and sign == '#'):
                current_letter = 0
                last_signe_was_hash = True
                dict_of_words[current_id] = [((y, x), current_letter)]
                board_horizontal[y, x] = current_id
                position_horizontal[y, x] = current_letter
            elif last_signe_was_hash and sign == '#':
                current_letter += 1
                dict_of_words[current_id].append(((y, x), current_letter))
                board_horizontal[y, x] = current_id
                position_horizontal[y, x] = current_letter
            elif last_signe_was_hash and sign != '#':
                current_id += 1
                current_letter = 0
                last_signe_was_hash = False
        if line[-1] == '#':
            current_id += 1
    for x in range(len(lines[0])):
        last_signe_was_hash = False
        for y in range(len(lines)):
            if (y == 0 and lines[y][x] == '#') or (not last_signe_was_hash and lines[y][x] == '#'):
                current_letter = 0
                last_signe_was_hash = True
                dict_of_words[current_id] = [((y, x), current_letter)]
                board_vertical[y, x] = current_id
                position_vertical[y, x] = current_letter
            elif last_signe_was_hash and lines[y][x] == '#':
                current_letter += 1
                dict_of_words[current_id].append(((y, x), current_letter))
                board_vertical[y, x] = current_id
                position_vertical[y, x] = current_letter
            elif last_signe_was_hash and lines[y][x] != '#':
                current_id += 1
                current_letter = 0
                last_signe_was_hash = False
        if lines[-1][x] == '#':
            current_id += 1

    for i in range(current_id):
        if dict_of_words[i][-1][1] == 0:
            del dict_of_words[i]

    board = np.ones((len(lines), len(lines[0]))).astype(int) * (-1)
    position_table = np.ones((len(lines), len(lines[0]))).astype(int) * (-1)
    for key in dict_of_words.keys():
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                if board_horizontal[y, x] == key:
                    board[y, x] = key
                    position_table[y, x] = position_horizontal[y, x]
                elif board_vertical[y, x] == key:
                    board[y, x] = key
                    position_table[y, x] = position_vertical[y, x]

    dict_of_relations = dict()
    for key, value in dict_of_words.items():
        dict_of_relations[key] = [value[-1][1] + 1, dict()]
        for temp_key, temp_value in dict_of_words.items():
            if temp_key != key:
                for my_yx, position in dict_of_words[key]:
                    for other_yx, _ in dict_of_words[temp_key]:
                        if my_yx == other_yx:
                            dict_of_relations[key][1][temp_key] = position
    return dict_of_relations, board, position_table


def is_correct(restrictions, solution):
    for i in restrictions.keys():
        if len(solution[i]) == restrictions[i][0]:
            for id, position in restrictions[i][1].items():
                try:
                    if solution[i][position] != solution[id][restrictions[id][1][i]]:
                        return False
                except:
                    return False

    return True


def print_solution(board, position, solution):
    print("-" * (board.shape[1] + 2))
    for y in range(board.shape[0]):
        line = "|"
        for x in range(board.shape[1]):
            if board[y, x] != -1:
                line += solution[board[y, x]][position[y, x]]
            else:
                line += ' '
        print(line + '|')
    print("-" * (board.shape[1] + 2))


def solve(crossword_shape):
    polish_words = [line.rstrip('\n') for line in open(r'polish_words.txt', encoding='UTF-8') if line != "\n"]
    random.shuffle(polish_words)
    for line in crossword_shape:
        print(line)
    restrictions, board, position = import_crossword_shape(crossword_shape)

    def DFS(partial_solution, to_solve):
        if not to_solve:
            return partial_solution
        # current word
        current_length, relations = restrictions[to_solve[0]]
        word_mask_list = [' ' for _ in range(current_length)]

        for id, position in relations.items():
            if id not in to_solve:
                word_mask_list[position] = partial_solution[id][restrictions[id][1][to_solve[0]]]
        word_mask = ""
        for letter in word_mask_list:
            word_mask+=letter

        for word in polish_words:
            if len(word)==current_length:
                is_good = True
                for i, letter in enumerate(word):
                    if word_mask[i]!=' ':
                        if letter!=word_mask[i]:
                            is_good=False
                            break
                if is_good:
                    p = partial_solution.copy()
                    p[to_solve[0]]=word
                    sol = DFS(p,to_solve[1:])
                    if sol:
                        return sol
        return dict()
    l = list(restrictions.keys())
    random.shuffle(l)
    solution = DFS(dict(),l)
    print_solution(board, position, solution)


if __name__ == "__main__":
    random.seed(1)
    crossword_shape = ["#####  ###", " #     # #", " #########", " #        ", "####      "]
    solve(crossword_shape)

    print("\n\n\n")

    random.seed(2)
    crossword_shape = ['###### ##### #####', ' #  #      # #    ', ' #  #      ###    ', ' #  ########      ', ' #       #      # ', ' #       #   #### ', '##########      # ', '         ######## ']
    solve(crossword_shape)


    # data representation
    # abstract_crossword_graph = {id : list[length,list of relations[tuple(id, number of letter)]]}

    # Algorithm:
    # DFS
