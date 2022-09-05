import numpy as np
import chess
from time import time


def ending_game(initial_state, mode='default'):
    def BFS(initial_position, mode='default', checked_positiones=set()):
        if mode == 'debug':
            queue = [["",initial_position.fen()]]
            while queue:
                path = queue.pop(0)
                node = chess.Board(path[1])

                for move in node.legal_moves:
                    new_board = node.copy()
                    new_board.push(move)
                    current_position = (new_board.fen()).split()
                    current_position = current_position[0] + " " + current_position[1]
                    if current_position not in checked_positiones:
                        checked_positiones.add(current_position)

                        if new_board.is_checkmate():
                            path[0] += str(move)
                            path[1] = new_board.fen()
                            return path

                        new_path = path.copy()
                        new_path[0] += str(move) + " "
                        new_path[1] = new_board.fen()

                        queue.append(new_path)
        elif mode == 'default':
            queue = [initial_position.fen()]
            while queue:
                board = chess.Board(queue.pop(0))

                for move in board.legal_moves:
                    board.push(move)
                    current_position = (board.fen()).split()
                    current_position = current_position[0] + " " + current_position[1]
                    if current_position not in checked_positiones:
                        checked_positiones.add(current_position)
                        if board.is_checkmate():
                            return board.halfmove_clock

                        queue.append(board.fen())

                    _ = board.pop()

    color, K, R, k = initial_state.split()
    d = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    board = chess.Board.empty()

    if color == 'black':
        board.turn = chess.BLACK
    else:
        board.turn = chess.WHITE

    board.set_piece_at(chess.square(d[K[0]], int(K[1]) - 1), chess.Piece.from_symbol('K'))
    board.set_piece_at(chess.square(d[R[0]], int(R[1]) - 1), chess.Piece.from_symbol('R'))
    board.set_piece_at(chess.square(d[k[0]], int(k[1]) - 1), chess.Piece.from_symbol('k'))
    if mode == 'default':
        return BFS(board, mode)

    elif mode == 'debug':
        print(BFS(board, mode)[0])

if __name__=="__main__":
    t_0 = time()
    ending_game('black h8 g8 a1', mode='debug')
    t_1 = time()
    print(t_1-t_0)