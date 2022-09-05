def tabliczka(x1, x2, y1, y2):
    max_length = len(str(x2 * y2)) + 1
    print(" " * max_length + ''.join([' ' * (max_length - len(str(l))) + str(l) for l in range(x1, x2 + 1)]))
    for y in range(y1, y2 + 1):
        print(" " * (max_length - len(str(y))) + str(y) + ''.join(
            [' ' * (max_length - len(str(l * y))) + str(l * y) for l in range(x1, x2 + 1)]))


if __name__ == '__main__':
    tabliczka(3, 5, 2, 4)
    print("\n")
    tabliczka(22, 33, 33, 50)
