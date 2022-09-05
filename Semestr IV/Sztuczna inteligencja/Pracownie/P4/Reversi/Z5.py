import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import random
from time import time, sleep
from queue import PriorityQueue
from tqdm.auto import tqdm


def v_board(board):
    plt.figure(figsize=(5, 5))
    plt.imshow(board, cmap="gist_earth")
    plt.xticks([])
    plt.yticks([])
    plt.show()


def v_game(game, trees, index, title):
    fig, ax = plt.subplots()
    ax.title.set_text(title)
    plt.subplots_adjust(left=0.25, bottom=0.25)
    ax.margins(x=0)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.imshow(game[0], cmap="gist_earth")
    axamp = plt.axes([0.25, 0.15, 0.65, 0.03])
    samp = Slider(axamp, 'Turn', 0, len(game) - 1, valinit=0, valstep=1)
    ax_two = plt.axes([0.25, 0.05, 0.65, 0.03])
    if trees[0]:
        s_two = Slider(ax_two, 'Considered', 0, len(trees[0].children), valinit=index, valstep=1)
    else:
        s_two = Slider(ax_two, 'Considered', 0, 0, valinit=index, valstep=1)
    def update(val):
        amp = samp.val
        if trees[amp]:
            s_two = Slider(ax_two, 'Considered', 0, len(trees[amp].children), valinit=index, valstep=1)
            ax.imshow(trees[amp].children[s_two.val].game, cmap="gist_earth")
        else:
            ax.imshow(game[amp], cmap="gist_earth")
        fig.canvas.draw_idle()

    samp.on_changed(update)
    s_two.on_changed(update)
    plt.show()


def init_board():
    board = np.zeros((8, 8)).astype(int)
    board[3, 3] = 1
    board[4, 4] = 1
    board[3, 4] = -1
    board[4, 3] = -1
    return board


def legal_moves(board, color):
    reachable = []
    for temp_y in range(8):
        for temp_x in range(8):
            if board[temp_y, temp_x] == 0:
                to_turn_over = []
                done = False
                for dir_x, dir_y in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    temp_to_turn_over = []
                    x = temp_x + dir_x
                    y = temp_y + dir_y
                    if x >= 0 and y >= 0 and x < 8 and y < 8:
                        temp_to_turn_over.append((y, x))
                        if board[y, x] == -1 * color:
                            x += dir_x
                            y += dir_y
                            while x >= 0 and y >= 0 and x < 8 and y < 8:
                                temp_to_turn_over.append((y, x))
                                if board[y, x] == -1 * color:
                                    x += dir_x
                                    y += dir_y
                                elif board[y, x] == 1 * color:
                                    to_turn_over += temp_to_turn_over
                                    done = True
                                    break
                                else:
                                    break
                if done:
                    temp_board = board.copy()
                    temp_board[temp_y, temp_x] = 1 * color
                    for y, x in to_turn_over:
                        temp_board[y, x] = 1 * color
                    reachable.append(temp_board)
    return reachable


def legal_move(board, color):
    ys, xs = np.where(board == 0)
    for temp_y, temp_x in zip(ys, xs):
        if True:
            if board[temp_y, temp_x] == 0:
                to_turn_over = []
                done = False
                for dir_x, dir_y in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    temp_to_turn_over = []
                    x = temp_x + dir_x
                    y = temp_y + dir_y
                    if x >= 0 and y >= 0 and x < 8 and y < 8:
                        temp_to_turn_over.append((y, x))
                        if board[y, x] == -1 * color:
                            x += dir_x
                            y += dir_y
                            while x >= 0 and y >= 0 and x < 8 and y < 8:
                                temp_to_turn_over.append((y, x))
                                if board[y, x] == -1 * color:
                                    x += dir_x
                                    y += dir_y
                                elif board[y, x] == 1 * color:
                                    to_turn_over += temp_to_turn_over
                                    done = True
                                    break
                                else:
                                    break
                if done:
                    temp_board = board.copy()
                    temp_board[temp_y, temp_x] = 1 * color
                    for y, x in to_turn_over:
                        temp_board[y, x] = 1 * color
                    return temp_board, True
    return board, False


def random_agent(board, color):
    order = [(y, x) for x in range(8) for y in range(8)]
    random.shuffle(order)
    for temp_y, temp_x in order:
        if board[temp_y, temp_x] == 0:
            to_turn_over = []
            done = False
            for dir_x, dir_y in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                temp_to_turn_over = []
                x = temp_x + dir_x
                y = temp_y + dir_y
                if x >= 0 and y >= 0 and x < 8 and y < 8:
                    temp_to_turn_over.append((y, x))
                    if board[y, x] == -1 * color:
                        x += dir_x
                        y += dir_y
                        while x >= 0 and y >= 0 and x < 8 and y < 8:
                            temp_to_turn_over.append((y, x))
                            if board[y, x] == -1 * color:
                                x += dir_x
                                y += dir_y
                            elif board[y, x] == color:
                                to_turn_over += temp_to_turn_over
                                done = True
                                break
                            else:
                                break
            if done:
                temp_board = board.copy()
                temp_board[temp_y, temp_x] = color
                for y, x in to_turn_over:
                    temp_board[y, x] = color
                return temp_board, True
    return board, False


def battle(Agent_1, Agent_2, number_of_games=1000, verbose=False):
    t_0 = time()
    number_of_first_Agent_wins = 0
    draws = 0
    for i in tqdm(range(number_of_games)):
        board = init_board()
        if verbose:
            game = [board]
        color = 1
        if i % 2 == 0:
            child, tree, index = Agent_1(board, color, 0)
            board = child.game
            moved = child.changed
        else:
            board, moved = Agent_2(board, color)
        stalemate = 0
        if verbose:
            game.append(board)
        turn = 1
        options = []
        trees = []
        while moved or stalemate < 2:
            turn += 1
            # if turn == 51:
            #     print("debug")
            color *= -1
            if i % 2 == 0:
                if color == -1:
                    board, moved = Agent_2(board, color)
                    print(turn, "agent 2", moved, stalemate)
                    index = 0
                    tree = []
                else:
                    print(turn, "agent 1", moved, stalemate)
                    child, tree, index = Agent_1(board, color, turn)
                    board = child.game
                    moved = child.changed
            else:
                if color == -1:
                    print(turn, "agent 1", moved, stalemate)
                    child, tree, index = Agent_1(board, color, turn)
                    board = child.game
                    moved = child.changed
                else:
                    board, moved = Agent_2(board, color)
                    tree = []
                    index = 0
                    print(turn, "agent 2", moved, stalemate)
            if not moved:
                stalemate += 1
            else:
                stalemate = 0
            if verbose:
                trees.append(tree)
                game.append(board)
        result = np.sum(board)
        if result != 0:
            if i % 2 == 0:
                number_of_first_Agent_wins += result > 0
            else:
                number_of_first_Agent_wins += result < 0
        else:
            draws += 1
        if verbose:
            # if verbose and ((i % 2 == 0 and result < 0) or (i % 2 == 1 and result > 0)):
            if i % 2 == 0:
                v_game(game, trees, index, "MCTS: white\n Result: " + str(int(np.sum(board) / 2 + 32)) + " to " + str(
                    32 - int(np.sum(board) / 2)))
            else:
                v_game(game, trees, index, "MCTS: black\n Result: " + str(32 - int(np.sum(board) / 2)) + " to " + str(
                    32 + int(np.sum(board) / 2)))
            verbose = False
    t_1 = time()
    if number_of_first_Agent_wins > (number_of_games - draws) / 2:
        print("First agent wins!")
    elif number_of_first_Agent_wins < (number_of_games - draws) / 2:
        print("First agent lost!")
    else:
        print("Draw!")
    print("MCTS won:", number_of_first_Agent_wins, ", lost:", number_of_games - number_of_first_Agent_wins - draws,
          "and draw", draws, "games. In time", t_1 - t_0)
    return number_of_games - number_of_first_Agent_wins - draws


def heuristic_1(board, color):
    importance = np.array([[18, -6, 1, 1, 1, 1, -6, 18],
                           [-6, -6, 1, 1, 1, 1, -6, -6],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [-6, -6, 1, 1, 1, 1, -6, -6],
                           [18, -6, 1, 1, 1, 1, -6, 18]])
    s = np.sum(np.abs(importance))
    return np.sum(board * importance) * color + s


def h_norm(l):
    m = np.min(l)
    M = np.max(l)
    if m == M:
        return np.ones(l.shape) * (1 / l.shape[0])
    temp_l = l - m
    return temp_l / np.sum(temp_l)


class Node:
    def __init__(self, current_game, current_color):
        self.game = current_game
        self.visited = False
        self.children = []
        self.parent = None
        self.number_of_visits = 0  # np.zeros(len(self.children)).astype(int)
        self.number_of_wins = 0  # np.zeros(len(self.children)).astype(int)
        self.color = current_color
        self.is_terminal = False
        self.changed = True
        self.heuristic_value = 0

    # def addNode(self, move, dist, opponent_trees, unusable):
    #     if move not in self.legal_moves:
    #         print("ERROR: not legal move!")
    #     else:
    #         self.legal_moves.remove(move)
    #         new_game = self.game.execute_move(move, opponent_trees)
    #         new_legal_moves = new_game.possible_moves(dist, opponent_trees, unusable)
    #         node = Node(new_game, new_legal_moves)
    #         node.current_move = move
    #         node.parent = self
    #         self.children.append(node)
    #         # if not self.legal_moves:
    #         #     self.game = None

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        if self.parent:
            index = self.parent.children.index(self)
            print(prefix + str((self.parent.heuristic_value[index])))

        if self.children:
            for child in self.children:
                child.print_tree()


def UCT(number_of_visits, number_of_wins, heuristics, c=10, q=0.5):
    zeros = np.where(number_of_visits == 0)
    if zeros[0].size == 0:
        total = np.sum(number_of_visits)
        v = h_norm((number_of_wins + np.abs(np.min(number_of_wins))) / number_of_visits + c * np.sqrt(
            np.log(total) / number_of_visits))
        final_vector = v * q + (1 - q) * heuristics
        return np.argmax(final_vector)
    else:
        return np.random.choice(zeros[0])
    # zeros = np.where(number_of_visits == 0)
    # if zeros[0].size==0:
    #     total = np.sum(number_of_visits)
    #     final_vector = number_of_wins/number_of_visits + c*np.sqrt(np.log(total)/number_of_visits)
    #     return np.argmax(final_vector)
    # else:
    #     return np.random.choice(zeros[0])


def select(tree, path):
    if tree.is_terminal:
        return tree
    if not tree.children:  # in other words - is a leaf
        if tree.visited:
            h_v = []
            for game in legal_moves(tree.game, tree.color):
                temp_node = Node(game, tree.color * (-1))
                temp_node.parent = tree
                temp_node.is_terminal = np.sum(temp_node.game == 0) == 0
                h_v.append(heuristic_1(temp_node.game, tree.color))
                tree.children.append(temp_node)
            if not tree.children:
                temp_node = Node(tree.game, tree.color * (-1))
                temp_node.parent = tree
                temp_node.is_terminal = tree.is_terminal
                temp_node.changed = False
                tree.children.append(temp_node)
                path.append(0)
                tree.number_of_wins = np.array([0]).astype(int)
                tree.number_of_visits = np.array([0]).astype(int)
                tree.heuristic_value = h_norm(np.array([heuristic_1(temp_node.game, tree.color)]))
                return temp_node
            tree.heuristic_value = h_norm(np.array(h_v))
            tree.number_of_visits = np.zeros(len(tree.children)).astype(int)
            tree.number_of_wins = np.zeros(len(tree.children)).astype(int)
            path.append(0)
            return tree.children[0]
        else:
            tree.visited = True
            return tree
    else:
        index = UCT(tree.number_of_visits, tree.number_of_wins, tree.heuristic_value)
        path.append(index)
        child = tree.children[index]
        return select(child, path)


def simulation(node):
    temp_board, moved = legal_move(node.game, node.color)
    first_time = False
    color = node.color
    while moved or first_time:
        color *= -1
        temp_board, moved = legal_move(temp_board, color)
        if moved:
            first_time = True
        else:
            first_time = False
    return np.sum(temp_board)


def backpropagation(node, payout, path):
    while node.parent:
        index = path.pop(-1)
        node.parent.number_of_wins[index] += payout * node.parent.color
        node.parent.number_of_visits[index] += 1
        node = node.parent


def MCTS(board, color, turn):
    # list_of_moves = game.possible_moves(dist, opponent_trees, unusable)
    tree = Node(board, color)
    h_v = []
    for game in legal_moves(tree.game, tree.color):
        temp_node = Node(game, tree.color * (-1))
        temp_node.parent = tree
        temp_node.is_terminal = np.sum(temp_node.game == 0) == 0
        tree.children.append(temp_node)
        h_v.append(heuristic_1(temp_node.game, tree.color))
    if not tree.children:
        temp_node = Node(tree.game,tree.color*(-1))
        temp_node.changed = False
        tree.children = [temp_node]
        tree.heuristic_value = np.array([0.5])
        return temp_node, tree, 0
    tree.heuristic_value = h_norm(np.array(h_v))
    tree.number_of_visits = np.zeros(len(tree.children)).astype(int)
    tree.number_of_wins = np.zeros(len(tree.children)).astype(int)
    tree.visited = True

    count = 0
    t = 0.5
    t_0 = time()

    while True:
        count += 1
        # SELECTION
        if time() - t_0 > t:
            break
        path = []
        # if turn == 51:
        #     print("select")
        node = select(tree, path)
        # SIMULATION
        # if turn == 51:
        #     print("simulation")
        if not node.is_terminal:
            payout = simulation(node)
        else:
            payout = np.sum(node.game)

        # BACKPROPAGATION
        # if turn == 51:
        #     print("backpropagation")
        backpropagation(node, payout, path)
    # print("Number of nodes:", count)
    # tree.print_tree()
    # sleep(1000)
    # print(count, file=sys.stderr, flush=True)
    move_id = np.argmax((tree.number_of_wins + 0.01) / (tree.number_of_visits + 0.01))
        # if move_id >= len(tree.children):
        #     child
        #     return np.random.choice(tree.children).game, tree.children[move_id].changed, move_id
    return tree.children[move_id], tree, move_id


if __name__ == '__main__':
    for i in range(10):
        np.random.seed(i)
        random.seed(i)
        battle(MCTS, random_agent, number_of_games=1, verbose=True)

    # MCTS: 1
    # Random: 9
