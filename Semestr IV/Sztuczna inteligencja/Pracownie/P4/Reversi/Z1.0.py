import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import random
from time import time
from queue import PriorityQueue
from tqdm.auto import tqdm


def v_board(board):
    plt.figure(figsize=(5, 5))
    plt.imshow(board, cmap="gist_earth")
    plt.xticks([])
    plt.yticks([])
    plt.show()


def v_game(game, title):
    fig, ax = plt.subplots()
    ax.title.set_text(title)
    plt.subplots_adjust(left=0.25, bottom=0.25)
    ax.margins(x=0)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.imshow(game[0], cmap="gist_earth")
    axamp = plt.axes([0.25, 0.15, 0.65, 0.03])
    samp = Slider(axamp, 'Turn', 0, len(game) - 1, valinit=0, valstep=1)

    def update(val):
        amp = samp.val
        ax.imshow(game[amp], cmap="gist_earth")
        fig.canvas.draw_idle()

    samp.on_changed(update)
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


def battle(Agent_1, Agent_2, hiperparamiters, number_of_games=1000, verbose=False):
    t_0 = time()
    number_of_first_Agent_wins = 0
    draws = 0
    for i in range(number_of_games):
        board = init_board()
        if verbose:
            game = [board]
        color = 1
        if i % 2 == 0:
            board, moved = Agent_1(board, color, hiperparamiters)
        else:
            board, moved = Agent_2(board, color)
        stalemate = 0
        if verbose:
            game.append(board)
        while moved or stalemate != 2:
            color *= -1
            if i % 2 == 0:
                if color == -1:
                    board, moved = Agent_2(board, color)
                else:
                    board, moved = Agent_1(board, color, hiperparamiters)
            else:
                if color == -1:
                    board, moved = Agent_1(board, color, hiperparamiters)
                else:
                    board, moved = Agent_2(board, color)
            if not moved:
                stalemate += 1
            else:
                stalemate = 0
            if verbose:
                game.append(board)
        result = np.sum(board)
        if result != 0:
            if i % 2 == 0:
                number_of_first_Agent_wins += result > 0
            else:
                number_of_first_Agent_wins += result < 0
        else:
            draws += 1

        if verbose and ((i % 2 == 0 and result < 0) or (i % 2 == 1 and result > 0)):
            if i % 2 == 0:
                v_game(game, "Agent 1: white\n Result: " + str(int(np.sum(board) / 2 + 32)) + " to " + str(
                    32 - int(np.sum(board) / 2)))
            else:
                v_game(game, "Agent 1: black\n Result: " + str(32 - int(np.sum(board) / 2)) + " to " + str(
                    32 + int(np.sum(board) / 2)))
            verbose = False
    t_1 = time()
    if number_of_first_Agent_wins > (number_of_games - draws) / 2:
        print("First agent wins!")
    elif number_of_first_Agent_wins < (number_of_games - draws) / 2:
        print("First agent lost!")
    else:
        print("Draw!")
    print("Agent 1 won:", number_of_first_Agent_wins, ", lost:", number_of_games - number_of_first_Agent_wins - draws,
          "and draw", draws, "games. In time", t_1 - t_0)
    return number_of_games - number_of_first_Agent_wins - draws


def Agent_1(board, color, hiperparamiters):
    bonus, penalty = hiperparamiters
    # if you can place piece in corner, do it
    # choose move that gives you the most pieces
    # bonus for piece on side +5
    # penalty for piece on side and neighboring corner -5
    queue = PriorityQueue()
    initial_val = np.sum(board)
    order = [(y, x) for x in range(8) for y in range(8)]
    order.remove((0, 0))
    order.remove((0, 7))
    order.remove((7, 0))
    order.remove((7, 7))
    random.shuffle(order)
    new_order = [(0, 0), (0, 7), (7, 0), (7, 7)] + order
    for temp_y, temp_x in new_order:
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
                if (temp_y, temp_x) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                    return temp_board, True

                val = np.sum(temp_board)
                val = (val - initial_val) * color
                if temp_x == 0 or temp_y == 0 or temp_x == 7 or temp_y == 7:
                    val += bonus
                if (temp_y, temp_x) in [(0, 1), (1, 0), (0, 6), (6, 0), (6, 7), (7, 6), (7, 1), (1, 7)]:
                    val -= penalty + bonus
                elif (temp_y, temp_x) in [(1, 1), (1, 6), (6, 1), (6, 6)]:
                    val -= penalty
                val += np.random.random()
                queue.put((-val, temp_board))

    if queue.empty():
        return board, False
    else:
        return queue.get()[1], True


def heuristic_1(board,importance):
    # importance = np.array([[8, -3, 3, 3, 3, 3, -3, 8],
    #                        [-3, -3, 1, 1, 1, 1, -3, -3],
    #                        [3, 1, 1, 1, 1, 1, 1, 3],
    #                        [3, 1, 1, 1, 1, 1, 1, 3],
    #                        [3, 1, 1, 1, 1, 1, 1, 3],
    #                        [3, 1, 1, 1, 1, 1, 1, 3],
    #                        [-3, -3, 1, 1, 1, 1, -3, -3],
    #                        [8, -3, 3, 3, 3, 3, -3, 8]])
    return np.sum(board * importance)


def Agent_2(board, color, hiperparamiters):
    depth, heuristic_function, importance = hiperparamiters

    def MinMax(board, current_color, max_depth, is_my_turn=False):
        if max_depth == 0:
            return heuristic_function(board,importance) * current_color * (-1)
        else:
            if is_my_turn:
                queue = PriorityQueue()
                for new_board in legal_moves(board, current_color):
                    queue.put(MinMax(new_board,current_color*(-1),max_depth,not is_my_turn)+np.random.random())
                if queue.empty():
                    return heuristic_function(board,importance)
                return queue.get()
            else:
                results = []
                for new_board in legal_moves(board, current_color):
                    results.append(MinMax(new_board,current_color*(-1),max_depth-1,not is_my_turn))
                if not results:
                    return heuristic_function(board,importance)
                return sum(results)/len(results)

    queue = PriorityQueue()
    for new_board in legal_moves(board, color):
        heuristic_value = MinMax(new_board, color * (-1), depth)
        # print(heuristic_value.shape)
        # print(heuristic_value)
        # print(int(heuristic_value))
        # print(new_board)
        queue.put((heuristic_value+np.random.random(),new_board))

    if queue.empty():
        return board, False
    else:
        return queue.get()[1], True

def generate_weighted_boards():
    l = []
    for corner in range(5):
        for corner_neighbour in range(-4, 0):
            for side in range(4):
                for middle in range(3):
                    for center in range(4):
                        board_up = np.array([[corner,corner_neighbour,side,side],
                                             [corner_neighbour,corner_neighbour,middle,middle],
                                             [side,middle,middle,center],
                                             [side,middle,center,center]])

                        board_down = np.array([[side,middle,center,center],
                                               [side,middle,middle,center],
                                               [corner_neighbour,corner_neighbour,middle,middle],
                                               [corner,corner_neighbour,side,side]])

                        total_left = np.vstack([board_up,board_down])
                        # np.rot90(board_up)
                        total_right = np.vstack([board_down.T,np.rot90(np.rot90(board_up))])
                        l.append(np.hstack([total_left,total_right]))
    return l

if __name__ == '__main__':
    # np.random.seed(0)
    # random.seed(0)
    battle(Agent_1, random_agent, (0, 6), number_of_games=50, verbose=False) # 77 loses / 1000 games tested in 50k reps
    # loses = []
    # for i, importance_board in tqdm(enumerate(generate_weighted_boards())):
    #     if i in [348,541,565,684,696,744,745,757,852,901,902,905,937,949,950,954]:
    #         loses.append(battle(Agent_2, random_agent, (1,heuristic_1,importance_board), number_of_games=500, verbose=False))
    # print(loses)
    # print(repr(loses))
    # loses = np.zeros((12, 12))
    # for bonus in tqdm(range(12)):
    #     for penalty in tqdm(range(12)):
    #         if bonus > 6 or penalty > 6:
    #             loses[bonus, penalty] = battle(Agent_1, random_agent, (bonus, penalty), number_of_games=2000,
    #                                            verbose=False)
    # print(repr(loses))
    # print(loses)

    # board = init_board()
    # game = [board]
    # color = 1
    # reachable = legal_moves(board,color)
    # while reachable:
    #     board = random.choice(reachable)
    #     game.append(board)
    #     color = color * (-1)
    #     reachable = legal_moves(board,color)
    #     # print(len(reachable))
    #     # v_board(board)
    # v_game(game)
