import numpy as np


def rozwiązanie_sudoku(given_matrix):
    # Idea:
    # - convert sudoku to problem of exact cover
    # - use Knuth's Algorithm X to solve it
    # https://en.wikipedia.org/wiki/Exact_cover -> Sudoku paragraph
    # https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X
    #
    # I have tried to describe this algorithm in details here, but it is
    # too long and too complicated for a single note. My program is
    # based on ideas from those two wikipedia pages above. If there will
    # be any ambiguity in my code, I can resolve it on our meting.

    def sub_alg(sets, original_indexes):
        # original_indexes are connecting constrains to the real numbers on
        # represented on sudoku.
        if sets.size == 0:
            # There are no constraints left to satisfy -> backpropagate success
            return [-1]

        # Sort columns by number of ones
        # It is a heuristic based on the idea that it might be better to satisfy
        # first constrains with fewer number of solutions.
        sets = (sets.T[np.argsort(sets.sum(axis=0))]).T

        rows = sets[sets[:, 0] == 1]
        objective_row_numbers = original_indexes[sets[:, 0] == 1]

        if rows.size == 0:
            # There is no item that solve chosen constraint -> backpropagate failure
            return []

        solution = []
        for i, objective_row_number in enumerate(objective_row_numbers):
            sets_c, new_indexes = remove_intersections(sets, original_indexes, rows, i)

            previous_solution = sub_alg(sets_c, new_indexes)

            if previous_solution == [-1]:
                solution.append([objective_row_number])

            elif previous_solution:
                # Backpropagation of funded solutions and merging them with current move
                solution += [partial_solution + [objective_row_number] for partial_solution in previous_solution]

        return sorted([sorted(s) for s in solution])

    solution = sub_alg(given_matrix, np.arange(given_matrix.shape[0]))
    if solution:
        return solution
    return None


def rozwiązanie_sudoku_first_solution(given_matrix, randomized=True):
    # Unlike algorithm above here I am not looking for all solutions to the sudoku,
    # just the first one founded. It is a sub-function of sudoku generators
    # written below. The main sudoku solver - "rozwiązanie_sudoku" is deterministic,
    # however it is more preferable to see a random solution. It makes generated sudoku
    # random. Also this algorithm mostly works faster.
    def sub_alg(sets, original_indexes, randomized):
        if sets.shape == (0, 0):
            return [-1]

        if randomized:
            # Sort columns by number of ones
            sets = (sets.T[np.argsort(sets.sum(axis=0))]).T

        rows = sets[sets[:, 0] == 1]
        objective_row_numbers = original_indexes[sets[:, 0] == 1]

        if rows.size == 0:
            return []

        for i, objective_row_number in enumerate(objective_row_numbers):
            sets_c, new_indexes = remove_intersections(sets, original_indexes, rows, i)

            previous_solution = sub_alg(sets_c, new_indexes, randomized)

            if previous_solution == [-1]:
                return [objective_row_number]

            elif previous_solution:
                return previous_solution + [objective_row_number]
        return previous_solution

    if randomized:
        order = np.arange(given_matrix.shape[0])
        np.random.shuffle(order)
        return sub_alg(given_matrix[order], np.arange(given_matrix.shape[0])[order], randomized)
    else:
        return sub_alg(given_matrix, np.arange(given_matrix.shape[0]), randomized)


def remove_intersections(sets, sets_ids, selected_rows, id):
    # Sub-function for sudoku solvers
    # It is removing items which satisfy already satisfied constraint.
    # Also it is removing already satisfied constraint from remaining set.
    sets_c = sets.copy()
    d_c = sets_ids.copy()
    for j in np.arange(sets_c.shape[1])[selected_rows[id] == 1][::-1]:
        # removing each row which intersection with rows[i] is not empty
        k = sets_c[:, j] == 0
        sets_c = sets_c[k]
        d_c = d_c[k]
        # removing each column that rows[i] covers
        sets_c = np.delete(sets_c, j, axis=1)

    return sets_c, d_c


def sudoku_matrix_representation(grid):
    # Convert sudoku to constraint satisfaction problem
    # input:
    # grid = np.array([n,n]) full of integers from range 1 to n
    # or zeros representing empty squares

    size = grid.shape[0]

    # grid to coordinates and values
    coordinates_and_values = np.array([[x, y, grid[x, y]] for x in range(size) for y in range(size) if grid[x, y] != 0])

    Row_column = np.zeros([size ** 3, size ** 2])
    Row_number = np.zeros([size ** 3, size ** 2])
    Column_number = np.zeros([size ** 3, size ** 2])
    Box_number = np.zeros([size ** 3, size ** 2])

    indexes_of_rows_to_delete = []

    coordinates = np.array(
        [[x, y, z] for x in range(size) for y in range(size) for z in range(1, size + 1)])
    for x in range(size):
        for y in range(size):
            for z in range(1, size + 1):
                Box_number[x * size * size + y * size + z - 1, int(
                    int(x / np.sqrt(size)) + int(y / np.sqrt(size)) * np.sqrt(size)) * size + z - 1] = 1
                Row_column[x * size * size + y * size + z - 1, x * size + y] = 1
                Row_number[x * size * size + y * size + z - 1, x * size + z - 1] = 1
                Column_number[x * size * size + y * size + z - 1, y * size + z - 1] = 1

    # removing rows to match condition of given grid
    for x, y, z in coordinates_and_values:
        for i in range(size):
            if i + 1 != z:
                indexes_of_rows_to_delete.append([int(x * size * size + y * size + i)])

    coordinates = np.delete(coordinates, indexes_of_rows_to_delete, axis=0)
    Row_column = np.delete(Row_column, indexes_of_rows_to_delete, axis=0)
    Row_number = np.delete(Row_number, indexes_of_rows_to_delete, axis=0)
    Column_number = np.delete(Column_number, indexes_of_rows_to_delete, axis=0)
    Box_number = np.delete(Box_number, indexes_of_rows_to_delete, axis=0)

    # output:
    # tuple with two elements
    # first: np.array([n,3]), each row [x,y,z] represents coordinates (x,y) of number z
    # second: np.array([n,m]), matrix of constraints
    return coordinates, np.hstack([Row_column, Row_number, Column_number, Box_number])


def print_sudoku(grid=np.empty([0, 0]), solution=None, coordinates=None, size_of_grid=None):
    # input optional:
    # 1.
    # grid = np.array([n,n]) full of integers from 1 to n or 0 representing empty square
    # 2.
    # solution = np.array([n**2]) or list - list of numbers of rows of transcription matrix
    # coordinates = np.array([m,3]) - each row [x,y,z] is list of coordinates (x,y) of value z

    if grid.size > 0:
        for y in range(grid.shape[1]):
            s = ""
            for x in range(grid.shape[0]):
                if grid[y, x] != 0:
                    s += str(int(grid[y, x]))
                else:
                    s += "_"
                if x % np.sqrt(grid.shape[0]) == np.sqrt(grid.shape[0]) - 1 and x != grid.shape[0] - 1:
                    s += "|"
            if y % np.sqrt(grid.shape[1]) == np.sqrt(grid.shape[1]) - 1 and y != grid.shape[1] - 1:
                s += "\n" + (int(np.sqrt(grid.shape[0])) * "-" + "+") * int(np.sqrt(grid.shape[0]) - 1) + int(
                    np.sqrt(grid.shape[0])) * "-"
            print(s)
    else:
        print_sudoku(grid=grid_from_coordinates(solution, coordinates, size_of_grid))


def grid_from_coordinates(solution, coordinates, size_of_grid):
    # Reconvert constraint representation of sudoku to normal one.
    X = []
    Y = []
    Z = []
    for i in solution:
        x, y, z = coordinates[i]
        X.append(x)
        Y.append(y)
        Z.append(z)
    if size_of_grid:
        size = size_of_grid
    else:
        size = max(int(np.sqrt(len(X))), max(Z))
    grid = np.zeros([size, size])
    for x, y, z in zip(X, Y, Z):
        grid[x, y] = z
    return grid


def sudoku_solution_checker(coordinates, solution):
    # input:
    # coordinates = np.array([m,3]) - each row [x,y,z] is
    # a list of coordinates (x,y) and value z
    # solution = np.array([n]) or list - list of indexes of rows
    # from index_of_constraint_matrix

    def check_if_range(grid, size):
        if [l for l in [sorted(g) for g in grid] if l != range(1, size + 1)] != []:
            return False

    size = np.sqrt(solution.shape[0])

    if size % 1 != 0:
        return False

    size = int(size)

    grid = grid_from_coordinates(solution, coordinates)

    # check row-number
    if not check_if_range(grid, size):
        return False

    # check column number
    if not check_if_range(grid.T, size):
        return False

    # check box-number
    Box = np.zeros([size, size])
    numerator = [0] * size
    for y in range(size):
        for x in range(size):
            current = int(int(x / np.sqrt(size)) + int(y / np.sqrt(size)) * np.sqrt(size))
            Box[current, numerator[current]] = grid[x, y]
            numerator[current] += 1

    if not check_if_range(Box, size):
        return False

    return True


def sudoku_generator(size=9):
    # Idea of generating sudoku:
    # - create random fully filled sudoku
    # - while sudoku has one unique solution:
    # -     remove some number
    # - return last founded sudoku with one solution
    if int(np.sqrt(size)) % 1 != 0:
        print("Not valid size!")
        return False

    last_grid = np.zeros([size, size])
    grid = np.zeros([size, size])

    basic_coordinates, transcription_matrix = sudoku_matrix_representation(last_grid)
    basic_solution = np.array(rozwiązanie_sudoku_first_solution(transcription_matrix))
    np.random.shuffle(basic_solution)

    while True:
        last_grid = grid
        basic_solution = basic_solution[1:]
        grid = grid_from_coordinates(basic_solution, basic_coordinates, size_of_grid=size)
        coordinates, transcription_matrix = sudoku_matrix_representation(grid)
        if len(rozwiązanie_sudoku(transcription_matrix)) > 1:
            break
    return last_grid.astype(int)


def difficult_sudoku_generator(size=9):
    # Idea of generating sudoku:
    # - create random fully filled sudoku
    # - while True:
    # -     for each number in sudoku:
    # -         check if its removing doesn't change 'solution uniqueness' rule
    # -         if not, remove that number and break the for loop
    # -     if none number was removed - break
    # - return last founded sudoku with one solution
    #
    # It is definitely not the fastest way to find quite hard to solve sudoku,
    # moreover it also is not the way to find hardest sudoku, but it was simple to
    # write having sudoku solver.
    if int(np.sqrt(size)) % 1 != 0:
        print("Not valid size!")
        return False

    last_grid = np.zeros([size, size])

    basic_coordinates, transcription_matrix = sudoku_matrix_representation(last_grid)
    basic_solution = np.array(rozwiązanie_sudoku_first_solution(transcription_matrix))
    np.random.shuffle(basic_solution)

    while True:
        founded = False
        for i in range(basic_solution.shape[0]):
            if not founded:
                temp_solution = np.hstack([basic_solution[:i], basic_solution[i + 1:]])
                grid = grid_from_coordinates(temp_solution, basic_coordinates, size_of_grid=size)
                coordinates, transcription_matrix = sudoku_matrix_representation(grid)
                sol = rozwiązanie_sudoku(transcription_matrix)
                if len(sol) == 1:
                    founded = True
                    basic_solution = temp_solution
        if not founded:
            return grid_from_coordinates(basic_solution, basic_coordinates, size_of_grid=size).astype(int)


if __name__ == '__main__':
    print("Example 1: generating easy sudoku and solving it")
    sudoku = sudoku_generator(size=16)
    print_sudoku(grid=sudoku)
    coordinates, constraints = sudoku_matrix_representation(sudoku)
    solution = rozwiązanie_sudoku(constraints)
    print("")
    print_sudoku(solution=solution[0], coordinates=coordinates)

    print("\nExample 2: generating hard sudoku (with significantly less squares field) and solving it")
    # It might take few seconds, but it is due to sudoku generation, not solving.
    print("")
    sudoku = difficult_sudoku_generator()
    print_sudoku(grid=sudoku)
    coordinates, constraints = sudoku_matrix_representation(sudoku)
    solution = rozwiązanie_sudoku(constraints)
    print("")
    print_sudoku(solution=solution[0], coordinates=coordinates)

    print("\nExample 3: solving sudoku with no solution")
    print("")
    sudoku = np.array([[1, 0, 0, 0],
                       [0, 0, 2, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 1]])
    print_sudoku(grid=sudoku)
    coordinates, constraints = sudoku_matrix_representation(sudoku)
    solution = rozwiązanie_sudoku(constraints)
    print(solution)

    print("\nExample 4: solving sudoku with two different solutions")
    print("")
    sudoku = np.array([[0, 1, 0, 2],
                       [2, 0, 1, 0],
                       [0, 2, 0, 1],
                       [1, 0, 2, 0]])
    print_sudoku(grid=sudoku)
    coordinates, constraints = sudoku_matrix_representation(sudoku)
    solution = rozwiązanie_sudoku(constraints)
    print("")
    print_sudoku(solution=solution[0], coordinates=coordinates)
    print("")
    print_sudoku(solution=solution[1], coordinates=coordinates)

    # Reflections:
    # Algorithm X is a efficient way to solve constraint satisfaction problem. It does not check
    # all ~9^(60) combinations of numbers in sudoku to find whether it is solvable or not. Some
    # kind of heuristic reasoning and backpropagation in case of failure helps considering just
    # the 'potential' solutions.
    #
    # It is interesting that the way that this algorithm works is really imitating human reasoning.
    # When there are no obvious places to write a number we are making assumption and checking if
    # it will lead to solution or contradiction.
