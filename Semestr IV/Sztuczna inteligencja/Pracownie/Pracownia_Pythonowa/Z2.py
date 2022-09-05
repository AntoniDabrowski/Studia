import numpy as np
import itertools
from tqdm.auto import tqdm


def findsubsets(s, n):
    return list(itertools.combinations(s, n))


def import_riddle(line):
    first_word, operator, second_word, equal, solution = line.split()
    return first_word, operator, second_word, solution


def is_solved(all_letters, first_word, operator, second_word, solution):
    first_num = np.sum([all_letters[letter] * pow(10, i) for i, letter in enumerate(first_word[::-1])])
    second_num = np.sum([all_letters[letter] * pow(10, i) for i, letter in enumerate(second_word[::-1])])
    solution_num = np.sum([all_letters[letter] * pow(10, i) for i, letter in enumerate(solution[::-1])])
    if operator == "+":
        return first_num + second_num == solution_num
    elif operator == "-":
        return first_num - second_num == solution_num
    elif operator == "*":
        return first_num - second_num == solution_num


def solve(line):
    first_word, operator, second_word, solution = import_riddle(line)
    all_letters = {letter: 0 for letter in first_word + second_word + solution}
    list_of_keys = list(all_letters.keys())

    for subset in tqdm(findsubsets({0, 1, 2, 3, 4, 5, 6, 7, 8, 9}, len(all_letters))[::-1]):
        for permutation in list(itertools.permutations(subset)):
            for i, num in enumerate(permutation):
                all_letters[list_of_keys[i]] = num
            if all_letters[first_word[0]] != 0 and all_letters[second_word[0]] != 0 and all_letters[solution[0]] != 0:
                if is_solved(all_letters, first_word, operator, second_word, solution):
                    return all_letters
    return dict()


if __name__ == '__main__':
    d1 = solve("send + more = money")
    d2 = solve("ciacho + ciacho = nadwaga")
    print(d1)
    print(d2)
