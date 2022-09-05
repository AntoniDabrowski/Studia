import sys
import math
from enum import Enum
import random
import numpy as np


class Cell:
    def __init__(self, cell_index, richness, neighbors):
        self.cell_index = cell_index
        self.richness = richness
        self.neighbors = neighbors


class Tree:
    def __init__(self, cell_index, size, is_mine, is_dormant):
        self.cell_index = cell_index
        self.size = size
        self.is_mine = is_mine
        self.is_dormant = is_dormant


class ActionType(Enum):
    WAIT = "WAIT"
    SEED = "SEED"
    GROW = "GROW"
    COMPLETE = "COMPLETE"


class Action:
    def __init__(self, type, target_cell_id=None, origin_cell_id=None):
        self.type = type
        self.target_cell_id = target_cell_id
        self.origin_cell_id = origin_cell_id

    def __str__(self):
        if self.type == ActionType.WAIT:
            return 'WAIT'
        elif self.type == ActionType.SEED:
            return f'SEED {self.origin_cell_id} {self.target_cell_id}'
        else:
            return f'{self.type.name} {self.target_cell_id}'

    @staticmethod
    def parse(action_string):
        split = action_string.split(' ')
        if split[0] == ActionType.WAIT.name:
            return Action(ActionType.WAIT)
        if split[0] == ActionType.SEED.name:
            return Action(ActionType.SEED, int(split[2]), int(split[1]))
        if split[0] == ActionType.GROW.name:
            return Action(ActionType.GROW, int(split[1]))
        if split[0] == ActionType.COMPLETE.name:
            return Action(ActionType.COMPLETE, int(split[1]))


class Game:
    def __init__(self):
        self.day = 0
        self.nutrients = 0
        self.board = []
        self.trees = []
        self.possible_actions = []
        self.my_sun = 0
        self.my_score = 0
        self.opponent_sun = 0
        self.opponent_score = 0
        self.opponent_is_waiting = 0

    def possible_moves(self, dist):
        list_of_moves = []

        # PRECOMPUTATION
        number_of_trees = {0: 0, 1: 0, 2: 0, 3: 0}
        # calculate number of each size tree (my tree)
        busy_cells = []
        for tree in self.trees:
            busy_cells.append(tree.cell_index)
            if tree.is_mine:
                number_of_trees[tree.size] += 1

        # WAIT
        list_of_moves.append("WAIT")

        # SEED

        # if number of seeds is less or equal to number of sun points
        if number_of_trees[0] <= self.my_sun:
            # for each not dormant tree
            for tree in self.trees:
                if tree.is_mine:
                    # for each destination
                    for i in range(37):
                        if i != tree.cell_index and dist[i, tree.cell_index] <= tree.size:
                            # if cell is not busy
                            if i not in busy_cells:
                                # add seed action on this cell to list_of_moves
                                list_of_moves.append("SEED " + str(tree.cell_index) + " " + str(i))

        # GROW

        # for each tree
        for tree in self.trees:
            # if tree is not dormant
            if not tree.is_dormant and tree.size != 3 and tree.is_mine:
                # if I have enough sun points
                if tree.size ** 2 + tree.size + 1 + number_of_trees[tree.size + 1] <= self.my_sun:
                    # add grow action on this tree to list_of_moves
                    list_of_moves.append("GROW " + str(tree.cell_index))

        # COMPLETE

        # for each tree
        for tree in self.trees:
            if not tree.is_dormant and tree.size == 3 and tree.is_mine:
                # if I have enough sun points
                if self.my_sun >= 4:
                    # add complete action on this tree to list_of_moves
                    list_of_moves.append("COMPLETE " + str(tree.position))
        return list_of_moves

    def execute_move(self, move):
        game = Game()
        if move.split()[0] == "WAIT":
            game.day = self.day + 1
            game.nutrients = self.nutrients
            game.board = self.board
            game.trees = self.trees
            game.possible_actions = []
            game.my_sun = self.my_sun  # + !!!!!!!!!!!!!
            game.my_score = self.my_score
            game.opponent_sun = self.opponent_sun  # + !!!!!!!!!
            game.opponent_score = self.opponent_score
            game.opponent_is_waiting = self.opponent_is_waiting
        elif move.split()[0] == "GROW":
            tree_to_grow = move.split()[0]
            tree_size = -1
            number_of_trees = {0: 0, 1: 0, 2: 0, 3: 0}
            # calculate number of each size tree (my tree)
            for tree in self.trees:
                if tree.cell_index == tree_to_grow:
                    tree_size = tree.size
                    tree.is_dormant = True
                if tree.is_mine:
                    number_of_trees[tree.size] += 1
            cost = tree_size ** 2 + tree_size + 1 + number_of_trees[tree_size]
            game.day = self.day
            game.nutrients = self.nutrients
            game.board = self.board
            game.trees = self.trees
            game.possible_actions = []
            game.my_sun = self.my_sun - cost
            game.my_score = self.my_score
            game.opponent_sun = self.opponent_sun
            game.opponent_score = self.opponent_score
            game.opponent_is_waiting = self.opponent_is_waiting
        elif move.split()[0] == "COMPLETE":
            game.day = self.day + 1
            game.nutrients = 0
            game.board = []
            game.trees = []
            game.possible_actions = []
            game.my_sun = 0
            game.my_score = 0
            game.opponent_sun = 0
            game.opponent_score = 0
            game.opponent_is_waiting = 0
        elif move.split()[0] == "SEED":
            game.day = self.day + 1
            game.nutrients = 0
            game.board = []
            game.trees = []
            game.possible_actions = []
            game.my_sun = 0
            game.my_score = 0
            game.opponent_sun = 0
            game.opponent_score = 0
            game.opponent_is_waiting = 0
        else:
            print("ERROR: wrong move!", file=sys.stderr, flush=True)
        return game

    def compute_next_action(self):
        return self.possible_actions[0]


class Game_simplified:
    def __init__(self):
        self.my_trees = np.zeros((4, 37)).astype(bool)
        self.dormants = np.zeros(37).astype(bool)
        self.my_sun = 0
        self.my_score = 0
        self.nutrient = 20
        self.day = 0

    def possible_moves(self, dist, opponent_trees, unusable):
        list_of_moves = []

        # PRECOMPUTATION
        number_of_trees = {0: np.sum(self.my_trees[0]), 1: np.sum(self.my_trees[1]), 2: np.sum(self.my_trees[2]),
                           3: np.sum(self.my_trees[3])}
        # calculate number of each size tree (my tree)
        busy_cells = np.logical_or(np.logical_or(self.my_trees.any(axis=0), opponent_trees.any(axis=0)), unusable)

        # WAIT
        list_of_moves.append("WAIT")

        # SEED

        # if number of seeds is less or equal to number of sun points
        if number_of_trees[0] <= self.my_sun:
            for size in range(1, 4):
                for i in range(37):
                    if my_trees[size, i] and not dormants[i]:
                        for dest in range(37):
                            if dest != i and dist[dest, i] <= size and not busy_cells[dest]:
                                list_of_moves.append("SEED " + str(i) + " " + str(dest))

        # GROW
        for size in range(3):
            if size ** 2 + size + 1 + number_of_trees[size + 1] <= self.my_sun:
                for cell_index in range(37):
                    if my_trees[size, cell_index] and not dormants[cell_index]:
                        list_of_moves.append("GROW " + str(cell_index))

        # COMPLETE

        if self.my_sun >= 4:
            for i in range(37):
                if my_trees[3, i]:
                    list_of_moves.append("COMPLETE " + str(i))
        return list_of_moves

    def execute_move(self, move, opponent_trees):
        game = Game_simplified()
        if move.split()[0] == "WAIT":
            if self.day+1==24:
                game.day = self.day + 1
                game.dormants = self.dormants
                game.nutrient = self.nutrient
                game.my_sun = self.my_sun
                game.my_trees = self.my_trees
                game.my_score = self.my_score
                return game
            game.day = self.day+1
            x = 0
            y = 0
            z = 0
            if game.day % 6 == 0:
                x += 1
                y -= 1
            elif game.day % 6 == 1:
                x += 1
                z -= 1
            elif game.day % 6 == 2:
                y += 1
                z -= 1
            elif game.day % 6 == 3:
                y += 1
                x -= 1
            elif game.day % 6 == 4:
                z += 1
                x -= 1
            elif game.day % 6 == 5:
                z += 1
                y -= 1
            shadows = np.zeros((3,37)).astype(bool)
            for size in range(1, 4):
                for i in range(37):
                    if self.my_trees[size, i] or opponent_trees[size, i]:
                        for shadowed_square in get_shadowed_squares(i, x, y, z, size):
                            shadows[size - 1, shadowed_square] = True
            print("shadows:", file=sys.stderr, flush=True)
            print(arr_to_str(shadows[0]), file=sys.stderr, flush=True)
            print(arr_to_str(shadows[1]), file=sys.stderr, flush=True)
            print(arr_to_str(shadows[2]), file=sys.stderr, flush=True)
            game.my_sun = self.my_sun + np.sum(self.my_trees[1] & (~shadows[0]) & (~shadows[1]) & (~shadows[2]))
            game.my_sun += np.sum(self.my_trees[2] & (~shadows[1]) & (~shadows[2])) * 2
            game.my_sun += np.sum(self.my_trees[3] & (~shadows[2])) * 3
            game.my_score = self.my_score
            game.my_trees = my_trees
            game.nutrient = self.nutrient
            game.dormants = np.zeros(37).astype(bool)
        elif move.split()[0] == "GROW":
            cell_index = int(move.split()[1])
            game.my_sun = self.my_sun
            game.my_trees = self.my_trees
            if self.my_trees[0, cell_index]:
                game.my_sun -= 1
                game.my_sun -= np.sum(self.my_trees[1])
                game.my_trees[0, cell_index] = False
                game.my_trees[1, cell_index] = True
            elif self.my_trees[1, cell_index]:
                game.my_sun -= 2
                game.my_sun -= np.sum(self.my_trees[2])
                game.my_trees[1, cell_index] = False
                game.my_trees[2, cell_index] = True
            elif self.my_trees[2, cell_index]:
                game.my_sun -= 3
                game.my_sun -= np.sum(self.my_trees[3])
                game.my_trees[2, cell_index] = False
                game.my_trees[3, cell_index] = True
            game.dormants = self.dormants
            game.nutrient = self.nutrient
            game.dormants[cell_index] = True
            game.my_score = self.my_score
            game.day = self.day
        elif move.split()[0] == "COMPLETE":
            cell_index = int(move.split()[1])
            game.my_sun = self.my_sun - 4
            game.dormants = self.dormants
            game.day = self.day
            game.dormants[cell_index]=False
            game.my_score = self.my_score + self.nutrient
            if cell_index<19:
                game.my_score+=2
            elif cell_index<7:
                game.my_score+=4
            game.nutrient = self.nutrient-1
            game.my_trees = self.my_trees
            game.my_trees[3,cell_index] = False
        elif move.split()[0] == "SEED":
            from_cell = int(move.split()[1])
            to_cell = int(move.split()[2])
            game.my_trees = self.my_trees
            game.day = self.day
            game.dormants = self.dormants
            game.dormants[from_cell]=True
            game.dormants[to_cell]=True
            game.my_sun = self.my_sun - np.sum(game.my_trees[0])
            game.nutrient = self.nutrient
            game.my_trees[0,to_cell]=True
            game.my_score = self.my_score
        return game


def import_data():
    game.day = int(input())
    game.nutrients = int(input())
    sun, score = [int(i) for i in input().split()]
    game.my_sun = sun
    game.my_score = score
    opp_sun, opp_score, opp_is_waiting = [int(i) for i in input().split()]
    game.opponent_sun = opp_sun
    game.opponent_score = opp_score
    game.opponent_is_waiting = opp_is_waiting
    game.trees.clear()
    number_of_trees = int(input())
    for i in range(number_of_trees):
        inputs = input().split()
        cell_index = int(inputs[0])
        size = int(inputs[1])
        is_mine = inputs[2] != "0"
        is_dormant = inputs[3] != "0"
        game.trees.append(Tree(cell_index, size, is_mine == 1, is_dormant))

    number_of_possible_actions = int(input())
    game.possible_actions.clear()
    for i in range(number_of_possible_actions):
        possible_action = input()
        game.possible_actions.append(Action.parse(possible_action))
    return game


def precompute_distances(list_of_cells):
    dist = np.ones([37, 37]).astype(int) * 1000
    for i in range(37):
        dist[i, i] = 0
    unusable = []
    for cell in list_of_cells:
        if cell.richness == 0:
            unusable.append(cell.cell_index)
    for cell in list_of_cells:
        if cell.richness != 0:
            for neigh in cell.neighbors:
                if neigh not in unusable and neigh != -1:
                    dist[cell.cell_index, neigh] = 1
                    dist[neigh, cell.cell_index] = 1
    for k in range(37):
        for i in range(37):
            for j in range(37):
                if dist[i, j] > dist[i, k] + dist[k, j]:
                    dist[i, j] = dist[i, k] + dist[k, j]
    unusable_arr = np.zeros(37).astype(bool)
    for i in unusable:
        unusable_arr[i] = True
    return dist, unusable_arr


def to_xyz(cell_index):
    return [(0, 0, 0), (1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1), (2, -2, 0), (2, -1, -1),
            (2, 0, -2), (1, 1, -2), (0, 2, -2), (-1, 2, -1), (-2, 2, 0), (-2, 1, 1), (-2, 0, 2), (-1, -1, 2),
            (0, -2, 2), (1, -2, 1), (3, -3, 0), (3, -2, -1), (3, -1, -2), (3, 0, -3), (2, 1, -3), (1, 2, -3),
            (0, 3, -3),
            (-1, 3, -2), (-2, 3, -1), (-3, 3, 0), (-3, 2, 1), (-3, 1, 2), (-3, 0, 3), (-2, -1, 3), (-1, -2, 3),
            (0, -3, 3), (1, -3, 2), (2, -3, 1)][cell_index]


def from_xyz(x, y, z):
    return {(0, 0, 0): 0, (1, -1, 0): 1, (1, 0, -1): 2, (0, 1, -1): 3, (-1, 1, 0): 4, (-1, 0, 1): 5, (0, -1, 1): 6,
            (2, -2, 0): 7, (2, -1, -1): 8, (2, 0, -2): 9, (1, 1, -2): 10, (0, 2, -2): 11, (-1, 2, -1): 12,
            (-2, 2, 0): 13,
            (-2, 1, 1): 14, (-2, 0, 2): 15, (-1, -1, 2): 16, (0, -2, 2): 17, (1, -2, 1): 18, (3, -3, 0): 19,
            (3, -2, -1): 20,
            (3, -1, -2): 21, (3, 0, -3): 22, (2, 1, -3): 23, (1, 2, -3): 24, (0, 3, -3): 25, (-1, 3, -2): 26,
            (-2, 3, -1): 27,
            (-3, 3, 0): 28, (-3, 2, 1): 29, (-3, 1, 2): 30, (-3, 0, 3): 31, (-2, -1, 3): 32, (-1, -2, 3): 33,
            (0, -3, 3): 34,
            (1, -3, 2): 35, (2, -3, 1): 36}[(x, y, z)]


def get_shadowed_squares(cell_index, x, y, z, size):
    shadowed_squares = []
    x_c, y_c, z_c = to_xyz(cell_index)
    for _ in range(size):
        x_c += x
        y_c += y
        z_c += z
        if max(abs(x_c), abs(y_c), abs(z_c)) <= 3:
            shadowed_squares.append(from_xyz(x_c, y_c, z_c))
    return shadowed_squares


def initialization(list_of_trees):
    dormants = np.zeros(37).astype(bool)
    my_trees = np.zeros((4, 37)).astype(bool)
    opponent_trees = np.zeros((4, 37)).astype(bool)

    for tree in list_of_trees:

        if tree.is_mine:
            if tree.is_dormant:
                dormants[tree.cell_index] = True
            my_trees[tree.size, tree.cell_index] = True
        else:
            opponent_trees[tree.size, tree.cell_index] = True
    return my_trees, dormants, opponent_trees

def arr_to_str(arr):
    s=""
    for i in range(arr.shape[0]):
        s+=str(int(arr[i]))
        if (i+1)%10==0:
            s+=" "
    return s

# initialization
number_of_cells = int(input())
game = Game()
game_simple = Game_simplified()
for i in range(number_of_cells):
    cell_index, richness, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    game.board.append(Cell(cell_index, richness, [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5]))

dist, unusable = precompute_distances(game.board)
random.seed(1)
# main loop
while True:
    game = import_data()
    my_trees, dormants, opponent_trees = initialization(game.trees)
    game_simple.my_sun = game.my_sun
    game_simple.my_score = game.my_score
    game_simple.my_trees = my_trees
    game_simple.dormants = dormants
    game_simple.nutrient = game.nutrients
    game_simple.day = game.day

    list_of_moves = game_simple.possible_moves(dist, opponent_trees, unusable)
    print("List of moves:", file=sys.stderr, flush=True)
    for line in list_of_moves:
        print(line, file=sys.stderr, flush=True)
    random_move = random.choice(list_of_moves)
    print("Chosen move:"+random_move, file=sys.stderr, flush=True)
    new_game = game_simple.execute_move(random_move,opponent_trees)
    print("my_sun: " + str(new_game.my_sun), file=sys.stderr, flush=True)
    print("my_score:" + str(new_game.my_score), file=sys.stderr, flush=True)
    print("my_trees 0: " + arr_to_str(new_game.my_trees[0]), file=sys.stderr, flush=True)
    print("my_trees 1: " + arr_to_str(new_game.my_trees[1]), file=sys.stderr, flush=True)
    print("my_trees 2: " + arr_to_str(new_game.my_trees[2]), file=sys.stderr, flush=True)
    print("my_trees 3: " + arr_to_str(new_game.my_trees[3]), file=sys.stderr, flush=True)
    print("dormants:   " + arr_to_str(new_game.dormants), file=sys.stderr, flush=True)
    print("nutrient: " + str(new_game.nutrient), file=sys.stderr, flush=True)
    print("day: " + str(new_game.day), file=sys.stderr, flush=True)

    # l = ["","","","","","",""]
    # for i in range(37):
    #     l[0]+=str(int(my_trees[0,i]))+" "
    #     l[1]+=str(int(my_trees[1,i]))+" "
    #     l[2]+=str(int(my_trees[2,i]))+" "
    #     l[3]+=str(int(dormants[i]))+" "
    #     l[4]+=str(int(shadows[0,i]))+" "
    #     l[5]+=str(int(shadows[1,i]))+" "
    #     l[6]+=str(int(shadows[2,i]))+" "
    # print(l[0], file=sys.stderr, flush=True)
    # print(l[1], file = sys.stderr, flush = True)
    # print(l[2], file = sys.stderr, flush = True)
    # print(l[3], file = sys.stderr, flush = True)
    # print(l[4], file = sys.stderr, flush = True)
    # print(l[5], file = sys.stderr, flush = True)
    # print(l[6], file = sys.stderr, flush = True)

    # print("Possible moves:", file=sys.stderr, flush=True)
    # for element in game.possible_moves(dist):
    #     print(element, file=sys.stderr, flush=True)

    print(random_move)
