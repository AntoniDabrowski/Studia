import numpy as np


def solve(X, Y, K):
    queue = [(0, 0)]
    visited = {(0, 0): None}
    while queue:
        x, y = queue.pop(0)
        for new_x, new_y in [(0, y), (x, 0), (min(X, x + y), max(0, y - (X - x))), (max(0, x - (Y - y)), min(Y, y + x)),
                             (x, Y), (X, y)]:
            if (new_x, new_y) not in visited:
                if new_x == K or new_y == K:
                    l = [(new_x, new_y),(x,y)]
                    new_x = x
                    new_y = y
                    while visited[(new_x, new_y)]:
                        new_x, new_y = visited[(new_x, new_y)]
                        l.append((new_x, new_y))
                    return l[::-1]
                else:
                    visited[(new_x, new_y)] = (x, y)
                    queue.append((new_x, new_y))
    return []


if __name__ == "__main__":
    print(solve(5, 3, 4))
    print(solve(13, 3, 2))
    print(solve(10, 2, 3))
