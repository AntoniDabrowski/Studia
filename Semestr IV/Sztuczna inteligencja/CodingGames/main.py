import sys
import math
from enum import Enum
import random
import numpy as np
from time import time


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


# initialization
number_of_cells = int(input())
game = Game()
for i in range(number_of_cells):
    cell_index, richness, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    game.board.append(Cell(cell_index, richness, [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5]))

dist, unusable = precompute_distances(game.board)
random.seed(0)
np.random.seed(0)

count = 0
while True:
    t_0 = time()
    game = import_data()
    my_trees, dormants, opponent_trees = initialization(game.trees)
    if count == 0 or count == 2:
        print("WAIT")
    elif count==1:
        for action in game.possible_actions:
            if action.split()[0]=="GROW":
                print(action)
                break
    elif count == 3:
        for action in game.possible_actions:
            if action.split()[0] == "SEED" and dist[]

    count+=1

