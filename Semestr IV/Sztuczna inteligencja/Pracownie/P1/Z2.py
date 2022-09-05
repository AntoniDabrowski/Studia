import numpy as np
from time import time
from tqdm.notebook import tqdm
from random import shuffle
import random

polish_words = [line.rstrip('\n') for line in open(r'polish_words.txt', encoding='UTF-8') if line != "\n"]


def fragmentation(phrase):
    def alg(starting_position, considered_solutions, depth):
        if starting_position in considered_solutions:
            if considered_solutions[starting_position][1] is None:
                return None, None
            return considered_solutions[starting_position]
        if phrase[starting_position:] in polish_words:
            solution = ((len(phrase) - starting_position) ** 2, [len(phrase)])
            considered_solutions[starting_position] = solution
            return solution

        prefix_endings = [starting_position + i for i in range(1, min(len(phrase) - starting_position + 1, 30)) if
                          phrase[starting_position:starting_position + i] in polish_words]
        best_fragmentation = None
        best_fitness = 0

        if not prefix_endings:
            considered_solutions[starting_position] = (None, None)
            return None, None

        for suffix_beginning in prefix_endings:
            new_fragmentation = alg(suffix_beginning, considered_solutions, depth + 1)
            if new_fragmentation[1] is not None:
                considered_solution = [suffix_beginning] + new_fragmentation[1]
                considered_solution_fitness = new_fragmentation[0] + (starting_position - suffix_beginning) ** 2

                if best_fragmentation is None or best_fitness < considered_solution_fitness:
                    best_fragmentation = considered_solution
                    best_fitness = considered_solution_fitness
                    considered_solutions[starting_position] = (considered_solution_fitness, considered_solution)

        return best_fitness, best_fragmentation

    def fragmentation_to_string(founded_fragmentation):
        my_str = phrase[0:founded_fragmentation[1][0]]
        for i in range(1, len(founded_fragmentation[1])):
            my_str += " " + phrase[founded_fragmentation[1][i - 1]:founded_fragmentation[1][i]]
        return my_str

    return fragmentation_to_string(alg(0, {}, 0))


def fragmentation_2(phrase):
    def alg(starting_position, considered_solutions, depth):
        if starting_position in considered_solutions:
            if considered_solutions[starting_position][1] is None:
                return None, None
            return considered_solutions[starting_position]
        if phrase[starting_position:] in polish_words:
            solution = ((len(phrase) - starting_position) ** 2, [len(phrase)])
            considered_solutions[starting_position] = solution
            return solution

        prefix_endings = [starting_position + i for i in range(1, min(len(phrase) - starting_position + 1, 30)) if
                          phrase[starting_position:starting_position + i] in polish_words]
        shuffle(prefix_endings)

        best_fragmentation = None
        best_fitness = 0

        if not prefix_endings:
            considered_solutions[starting_position] = (None, None)
            return None, None

        for suffix_beginning in prefix_endings:
            new_fragmentation = alg(suffix_beginning, considered_solutions, depth + 1)
            if new_fragmentation is not None and new_fragmentation[1] is not None:
                considered_solution = [suffix_beginning] + new_fragmentation[1]
                considered_solution_fitness = new_fragmentation[0] + (starting_position - suffix_beginning) ** 2
                return considered_solution_fitness, considered_solution
                # if best_fragmentation is None or best_fitness < considered_solution_fitness:
                #     best_fragmentation = considered_solution
                #     best_fitness = considered_solution_fitness
                #     considered_solutions[starting_position] = (considered_solution_fitness, considered_solution)
        #
        # return best_fitness, best_fragmentation

    def fragmentation_to_string(founded_fragmentation):
        my_str = phrase[0:founded_fragmentation[1][0]]
        for i in range(1, len(founded_fragmentation[1])):
            my_str += " " + phrase[founded_fragmentation[1][i - 1]:founded_fragmentation[1][i]]
        return my_str

    return fragmentation_to_string(alg(0, {}, 0))


if __name__ == "__main__":
    # print(fragmentation('jakmniedzieckodozdrowiapowróciłaścudem'))
    # print(fragmentation_2('tamatematykapustkinieznosi'))
    random.seed(0)
    t_0 = time()
    with open("Pan_Tadeusz_bez_spacji.txt", 'r', encoding='UTF-8') as input_file, open("Pan_Tadeusz_losowy.txt", 'w',
                                                                                       encoding="UTF-8") as output_file:
        for i, line in enumerate(input_file.read().split()):
            if i % 50 == 10:
                t_1 = time()
                print("Current run time:", str((t_1 - t_0) / 60)[:6], "\nExpected time for rest:",
                      str((9943 - i) * (t_1 - t_0) / (i * 60))[:6])
            print(str(i * 100 / 9943)[:4] + "%")
            output_file.write(fragmentation_2(line) + "\n")
    t_1 = time()
    print(t_1 - t_0)
