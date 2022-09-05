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
                    if my_trees[size, i] and not self.dormants[i]:
                        for dest in range(37):
                            if dest != i and dist[dest, i] <= size and not busy_cells[dest]:
                                list_of_moves.append("SEED " + str(i) + " " + str(dest))

        # GROW
        for size in range(3):
            if size ** 2 + size + 1 + number_of_trees[size + 1] <= self.my_sun:
                for cell_index in range(37):
                    if my_trees[size, cell_index] and not self.dormants[cell_index]:
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
            if self.day + 1 == 24:
                game.day = self.day + 1
                game.dormants = self.dormants.copy()
                game.nutrient = self.nutrient
                game.my_sun = self.my_sun
                game.my_trees = self.my_trees.copy()
                game.my_score = self.my_score
                return game
            game.day = self.day + 1
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
            shadows = np.zeros((3, 37)).astype(bool)
            for size in range(1, 4):
                for i in range(37):
                    if self.my_trees[size, i] or opponent_trees[size, i]:
                        for shadowed_square in get_shadowed_squares(i, x, y, z, size):
                            shadows[size - 1, shadowed_square] = True
            # print("shadows:", file=sys.stderr, flush=True)
            # print(arr_to_str(shadows[0]), file=sys.stderr, flush=True)
            # print(arr_to_str(shadows[1]), file=sys.stderr, flush=True)
            # print(arr_to_str(shadows[2]), file=sys.stderr, flush=True)
            game.my_sun = self.my_sun + np.sum(self.my_trees[1] & (~shadows[0]) & (~shadows[1]) & (~shadows[2]))
            game.my_sun += np.sum(self.my_trees[2] & (~shadows[1]) & (~shadows[2])) * 2
            game.my_sun += np.sum(self.my_trees[3] & (~shadows[2])) * 3
            game.my_score = self.my_score
            game.my_trees = self.my_trees.copy()
            game.nutrient = self.nutrient
            game.dormants = np.zeros(37).astype(bool)

        elif move.split()[0] == "GROW":
            cell_index = int(move.split()[1])
            game.my_sun = self.my_sun
            game.my_trees = self.my_trees.copy()
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
            game.dormants = self.dormants.copy()
            game.nutrient = self.nutrient
            game.dormants[cell_index] = True
            game.my_score = self.my_score
            game.day = self.day

        elif move.split()[0] == "COMPLETE":
            cell_index = int(move.split()[1])
            game.my_sun = self.my_sun - 4
            game.dormants = self.dormants.copy()
            game.day = self.day
            game.dormants[cell_index] = False
            game.my_score = self.my_score + self.nutrient
            if cell_index < 19:
                game.my_score += 2
            elif cell_index < 7:
                game.my_score += 4
            game.nutrient = self.nutrient - 1
            game.my_trees = self.my_trees.copy()
            game.my_trees[3, cell_index] = False

        elif move.split()[0] == "SEED":
            from_cell = int(move.split()[1])
            to_cell = int(move.split()[2])
            game.my_trees = self.my_trees.copy()
            game.day = self.day
            game.dormants = self.dormants.copy()
            game.dormants[from_cell] = True
            game.dormants[to_cell] = True
            game.my_sun = self.my_sun - np.sum(game.my_trees[0])
            game.nutrient = self.nutrient
            game.my_trees[0, to_cell] = True
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
    s = ""
    for i in range(arr.shape[0]):
        s += str(int(arr[i]))
        if (i + 1) % 10 == 0:
            s += " "
    return s


class Node:
    def __init__(self, current_game, legal_moves):
        self.game = current_game
        self.legal_moves = legal_moves
        self.children = []
        self.parent = None
        self.number_of_visits = np.zeros(len(legal_moves)).astype(int)
        self.number_of_wins = np.zeros(len(legal_moves)).astype(int)
        self.current_move = "root"

    def addNode(self, move, dist, opponent_trees, unusable):
        if move not in self.legal_moves:
            print("ERROR: not legal move!", file=sys.stderr, flush=True)
        else:
            self.legal_moves.remove(move)
            new_game = self.game.execute_move(move, opponent_trees)
            new_legal_moves = new_game.possible_moves(dist, opponent_trees, unusable)
            node = Node(new_game, new_legal_moves)
            node.current_move = move
            node.parent = self
            self.children.append(node)
            # if not self.legal_moves:
            #     self.game = None

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level+=1
            p = p.parent
        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + self.current_move, file=sys.stderr, flush=True)
        # if self.current_move.split()[0]=="SEED":
            # print("dormants:   " + arr_to_str(self.game.dormants), file=sys.stderr, flush=True)
        if self.children:
            for child in self.children:
                child.print_tree()

def UCT(number_of_visits, number_of_wins,c=10):
    zeros = np.where(number_of_visits == 0)
    if zeros[0].size==0:
        total = np.sum(number_of_visits)
        final_vector = number_of_wins/number_of_visits + c*np.sqrt(np.log(total)/number_of_visits)
        return np.argmax(final_vector)
    else:
        return np.random.choice(zeros[0])

def select(tree,path):
    if tree.legal_moves:
        path.append(len(tree.children))
        return tree, np.random.choice(tree.legal_moves)
    else:
        index = UCT(tree.number_of_visits,tree.number_of_wins)
        path.append(index)
        child = tree.children[index]
        return select(child,path)

def simulation(node, dist, opponent_trees, unusable):
    game = Game_simplified()
    game.day = node.game.day
    game.my_sun = node.game.my_sun
    game.nutrient = node.game.nutrient
    game.my_score = node.game.my_score
    game.my_trees = node.game.my_trees.copy()
    game.dormants = node.game.dormants.copy()
    if game.day>24:
        return 0
    while game.day<24:
        move = np.random.choice(game.possible_moves(dist, opponent_trees, unusable))
        game = game.execute_move(move,opponent_trees)
    return game.my_score + (1 - 1/np.sum(game.my_trees)) + game.my_sun//3

def backpropagation(node,payout,path):
    while node.parent:
        node.number_of_wins[path.pop(-1)] += payout
        node = node.parent
    node.number_of_wins[path.pop(-1)] += payout

def MCTS(game, dist, opponent_trees, unusable,t_0):
    list_of_moves = game.possible_moves(dist, opponent_trees, unusable)
    tree = Node(game, list_of_moves)
    count = 0
    t = 0.08
    while True:
        count += 1
        # SELECTION
        if time()-t_0>t:
            break
        path = []
        node, move = select(tree,path)

        if time()-t_0>t:
            break
        # print(node.game.day, file=sys.stderr, flush=True)
        # print(1, file=sys.stderr, flush=True)
        # EXPANSION
        node.addNode(move, dist, opponent_trees, unusable)

        if time()-t_0>t:
            break
        # print(2, file=sys.stderr, flush=True)
        # SIMULATION
        payout = simulation(node.children[-1], dist, opponent_trees, unusable)

        if time()-t_0>t:
            break
        # print(3, file=sys.stderr, flush=True)
        # BACKPROPAGATION
        backpropagation(node,payout,path)

        # print(4, file=sys.stderr, flush=True)
    # tree.print_tree()
    # print(count, file=sys.stderr, flush=True)
    move_id = np.argmax((tree.number_of_wins+0.01)/(tree.number_of_visits+0.01))
    if move_id>=len(tree.children):
        return np.random.choice(tree.legal_moves)
    return tree.children[move_id].current_move



# initialization
number_of_cells = int(input())
game = Game()
game_simple = Game_simplified()
for i in range(number_of_cells):
    cell_index, richness, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    game.board.append(Cell(cell_index, richness, [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5]))

dist, unusable = precompute_distances(game.board)
random.seed(0)
np.random.seed(0)
# seed=-521199459321439810
# main loop
while True:
    t_0 = time()
    game = import_data()
    my_trees, dormants, opponent_trees = initialization(game.trees)
    game_simple.my_sun = game.my_sun
    game_simple.my_score = game.my_score
    game_simple.my_trees = my_trees
    game_simple.dormants = dormants
    game_simple.nutrient = game.nutrients
    game_simple.day = game.day
    chosen_move = MCTS(game_simple, dist, opponent_trees, unusable,t_0)
    print(chosen_move)
    # Debug: nie zgadzają się predykcjie; seed=-521199459321439810

    # print("List of moves:", file=sys.stderr, flush=True)
    # l = ""
    # for line in list_of_moves:
    #     l+=line+" "
    # print(l, file=sys.stderr, flush=True)
    # print("my_sun: " + str(tree.game.my_sun), file=sys.stderr, flush=True)
    # print("my_score:" + str(tree.game.my_score), file=sys.stderr, flush=True)
    # print("my_trees 0: " + arr_to_str(tree.game.my_trees[0]), file=sys.stderr, flush=True)
    # print("my_trees 1: " + arr_to_str(tree.game.my_trees[1]), file=sys.stderr, flush=True)
    # print("my_trees 2: " + arr_to_str(tree.game.my_trees[2]), file=sys.stderr, flush=True)
    # print("my_trees 3: " + arr_to_str(tree.game.my_trees[3]), file=sys.stderr, flush=True)
    # print("dormants:   " + arr_to_str(tree.game.dormants), file=sys.stderr, flush=True)
    # print("nutrient: " + str(tree.game.nutrient), file=sys.stderr, flush=True)
    # print("day: " + str(tree.game.day), file=sys.stderr, flush=True)

    # tree = Node(game_simple, list_of_moves)
    # while tree.legal_moves:
    #     move = tree.legal_moves[0]
    #     tree.addNode(tree.legal_moves[0], dist, opponent_trees, unusable)
        # print("my_trees 0 after move: "+move + arr_to_str(tree.children[-1].game.my_trees[0]), file=sys.stderr, flush=True)

    # for children in tree.children:
        # print("   |  ","Chosen move:" + children.current_move, file=sys.stderr, flush=True)
        # print("   |  ","List of moves:", file=sys.stderr, flush=True)
        # l = ""
        # for line in children.legal_moves:
        #     l+=line+" "
        # print("   |  ",l, file=sys.stderr, flush=True)
        # print("   |  ","my_sun: " + str(children.game.my_sun), file=sys.stderr, flush=True)
        # print("   |  ","my_score:" + str(children.game.my_score), file=sys.stderr, flush=True)
        # print("   |  ","my_trees 0: " + arr_to_str(children.game.my_trees[0]), file=sys.stderr, flush=True)
        # print("   |  ","my_trees 1: " + arr_to_str(children.game.my_trees[1]), file=sys.stderr, flush=True)
        # print("   |  ","my_trees 2: " + arr_to_str(children.game.my_trees[2]), file=sys.stderr, flush=True)
        # print("   |  ","my_trees 3: " + arr_to_str(children.game.my_trees[3]), file=sys.stderr, flush=True)
        # print("   |  ","dormants:   " + arr_to_str(children.game.dormants), file=sys.stderr, flush=True)
        # print("   |  ","nutrient: " + str(children.game.nutrient), file=sys.stderr, flush=True)
        # print("   |__","day: " + str(children.game.day), file=sys.stderr, flush=True)
        # while children.legal_moves:
        #     chosen = children.legal_moves[0]
        #     children.addNode(chosen, dist, opponent_trees, unusable)

            # print("      |  ","Chosen move:" + chosen, file=sys.stderr, flush=True)
            # print("      |  ","List of moves:", file=sys.stderr, flush=True)
            # l = ""
            # for line in children.children[-1].legal_moves:
            #     l+=line+" "
            # print("      |  ",l, file=sys.stderr, flush=True)
            # print("      |  ","my_sun: " + str(children.children[-1].game.my_sun), file=sys.stderr, flush=True)
            # print("      |  ","my_score:" + str(children.children[-1].game.my_score), file=sys.stderr, flush=True)
            # print("      |  ","my_trees 0: " + arr_to_str(children.children[-1].game.my_trees[0]), file=sys.stderr, flush=True)
            # print("      |  ","my_trees 1: " + arr_to_str(children.children[-1].game.my_trees[1]), file=sys.stderr, flush=True)
            # print("      |  ","my_trees 2: " + arr_to_str(children.children[-1].game.my_trees[2]), file=sys.stderr, flush=True)
            # print("      |  ","my_trees 3: " + arr_to_str(children.children[-1].game.my_trees[3]), file=sys.stderr, flush=True)
            # print("      |  ","dormants:   " + arr_to_str(children.children[-1].game.dormants), file=sys.stderr, flush=True)
            # print("      |  ","nutrient: " + str(children.children[-1].game.nutrient), file=sys.stderr, flush=True)
            # print("      |__","day: " + str(children.children[-1].game.day), file=sys.stderr, flush=True)

    # for _ in range(3):
    #     if list_of_moves:
    #         if random_move in list_of_moves:
    #             list_of_moves.remove(random_move)
    #         random_move = random.choice(list_of_moves)
    #         tree.addNode(random_move, dist, opponent_trees, unusable)
    #
    #         new_game = game_simple.execute_move(random_move, opponent_trees)
    #         temp_list_of_moves = new_game.possible_moves(dist, opponent_trees, unusable)
    #         temp_random_move = random.choice(list_of_moves)
    #         for _ in range(3):
    #             if temp_list_of_moves:
    #                 if temp_random_move in temp_list_of_moves:
    #                     temp_list_of_moves.remove(temp_random_move)
    #                 temp_random_move = random.choice(list_of_moves)
    #                 tree.children[-1].addNode(temp_random_move, dist, opponent_trees, unusable)

    # tree.print_tree()

    # print("List of moves:", file=sys.stderr, flush=True)
    # for line in list_of_moves:
    #     print(line, file=sys.stderr, flush=True)
    # print("Chosen move:"+random_move, file=sys.stderr, flush=True)
    # new_game = game_simple.execute_move(random_move,opponent_trees)
    # print("my_sun: " + str(new_game.my_sun), file=sys.stderr, flush=True)
    # print("my_score:" + str(new_game.my_score), file=sys.stderr, flush=True)
    # print("my_trees 0: " + arr_to_str(new_game.my_trees[0]), file=sys.stderr, flush=True)
    # print("my_trees 1: " + arr_to_str(new_game.my_trees[1]), file=sys.stderr, flush=True)
    # print("my_trees 2: " + arr_to_str(new_game.my_trees[2]), file=sys.stderr, flush=True)
    # print("my_trees 3: " + arr_to_str(new_game.my_trees[3]), file=sys.stderr, flush=True)
    # print("dormants:   " + arr_to_str(new_game.dormants), file=sys.stderr, flush=True)
    # print("nutrient: " + str(new_game.nutrient), file=sys.stderr, flush=True)
    # print("day: " + str(new_game.day), file=sys.stderr, flush=True)

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

