import numpy as np
import matplotlib.pyplot as plt


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
    temp_l = l-np.min(l)
    return temp_l/np.sum(temp_l)

def board_gen(num):
    return [np.random.randint(-1,2,(8,8)) for _ in range(num)]


if __name__ == '__main__':
    r = 100
    X = np.arange(r)+1
    Y = np.array([pow(1+1/n,n) for n in range(1,r+1)])
    plt.scatter(X,Y)
    plt.show()