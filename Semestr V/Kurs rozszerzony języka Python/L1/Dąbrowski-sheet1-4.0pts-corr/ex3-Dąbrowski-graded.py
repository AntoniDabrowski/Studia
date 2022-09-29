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

    # Grade: 2.0

    # Didactic notes:
    tabliczka(95, 120, 60, 100) # passes
    tabliczka(3, 5, 2, 4) # passes
    tabliczka(1, 1, 1, 1) # passes
    tabliczka(-10, 15, -15, 15) # does not pass, erases some spaces in the bottom left corner.

    # Personally, I find such a solution hard to read, even though it uses "Pythonic" components such as list
    # comprehension. I guess this is a common criticism of "Pythonic" code.
    # For the future, I would suggest being a bit less strict with the line code, and e.g.
    # assign this to a special variable and explain the variable (above it) with a one-line comment:
    # ''.join([' ' * (max_length - len(str(l))) + str(l) for l in range(x1, x2 + 1)])

    # As for the negative table, I agree that it is a natural assumption that the numbers are positive integers,
    # but in the task list it is absent (in neither Polish nor English). I am not deducting points by that, but keep
    # these assumptions in mind for the future.

