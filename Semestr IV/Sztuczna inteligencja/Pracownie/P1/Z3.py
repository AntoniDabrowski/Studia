import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm


def hands_comparison(hand_A, hand_B):
    hand_A = sorted(hand_A, key=lambda x: x[0])
    colors_A = np.array([element[1] for element in hand_A]) - min(hand_A, key=lambda x: x[1])[1]
    hand_A = np.array([element[0] for element in hand_A]) - min(hand_A, key=lambda x: x[0])[0]

    hand_B = np.array([element - min(hand_B) for element in sorted(hand_B)])

    if (hand_A == np.array([0, 1, 2, 3, 4])).all():
        if (colors_A == np.array([0, 0, 0, 0, 0])).all():
            score_A = 8
        else:
            score_A = 4
    elif (hand_A[:4] == np.array([0, 0, 0, 0])).all() or (
            hand_A[1] != 0 and (hand_A[1:] / hand_A[1] == np.array([1, 1, 1, 1])).all()):
        score_A = 7
    elif ((hand_A[:3] == np.array([0, 0, 0])).all() and (
            hand_A[3] != 0 and (hand_A[3:] / hand_A[3] == np.array([1, 1])).all())) or \
            (hand_A[2] != 0 and (hand_A[2:] / hand_A[2] == np.array([1, 1, 1])).all()) and (
            (hand_A[:2] == np.array([0, 0])).all()):
        score_A = 6
    elif (colors_A == np.array([0, 0, 0, 0, 0])).all():
        score_A = 5
    elif (hand_A[2] != 0 and (hand_A[2:] / hand_A[2] == np.array([1, 1, 1])).all()) or (
            hand_A[2] != 0 and (hand_A[1:4] / hand_A[2] == np.array([1, 1, 1])).all()) or (
            hand_A[:3] == np.array([0, 0, 0])).all():
        score_A = 3
    elif (hand_A[0] == hand_A[1] and hand_A[2] == hand_A[3]) or (hand_A[0] == hand_A[1] and hand_A[3] == hand_A[4]) or (
            hand_A[1] == hand_A[2] and hand_A[3] == hand_A[4]):
        score_A = 2

    elif (hand_A[0] == hand_A[1]) or (hand_A[1] == hand_A[2]) or (hand_A[2] == hand_A[3]) or (hand_A[3] == hand_A[4]):
        score_A = 1
    else:
        score_A = 0

    if (hand_B == np.array([0, 1, 2, 3, 4])).all():
        score_B = 4
    elif (hand_B[:4] == np.array([0, 0, 0, 0])).all() or (
            hand_B[1] != 0 and (hand_B[1:] / hand_B[1] == np.array([1, 1, 1, 1])).all()):
        score_B = 7
    elif ((hand_B[:3] == np.array([0, 0, 0])).all() and (
            hand_B[3] != 0 and (hand_B[3:] / hand_B[3] == np.array([1, 1])).all())) or (
            hand_B[2] != 0 and (hand_B[2:] / hand_B[2] == np.array([1, 1, 1])).all()) and (
            hand_B[:2] == np.array([0, 0])).all():
        score_B = 6
    elif (hand_B[2] != 0 and (hand_B[2:] / hand_B[2] == np.array([1, 1, 1])).all()) or (
            (hand_B[2] != 0 and hand_B[1:4] / hand_B[2] == np.array([1, 1, 1])).all()) or \
            (hand_B[:3] == np.array([0, 0, 0])).all():
        score_B = 3
    elif (hand_B[0] == hand_B[1] and hand_B[2] == hand_B[3]) or (hand_B[0] == hand_B[1] and hand_B[3] == hand_B[4]) or (
            hand_B[1] == hand_B[2] and hand_B[3] == hand_B[4]):
        score_B = 2
    else:
        score_B = 1

    return score_A, score_B


def estimate_winning_probability_1(deck_A, deck_B, no_of_iterations=200):
    winnings_of_A = 0
    winnings_of_B = 0
    solution = []

    # if deck_A is invalid returns immediate winning for player B
    if len(deck_A) < 5:
        return [1]

    for _ in range(no_of_iterations):
        hand_A = [deck_A[i] for i in np.random.choice(np.arange(len(deck_A)), 5, replace=False)]
        hand_B = np.random.choice(deck_B, 5, replace=False)
        score_A, score_B = hands_comparison(hand_A, hand_B)
        if score_A > score_B:
            winnings_of_A += 1
        else:
            winnings_of_B += 1
        solution.append(winnings_of_A / (winnings_of_A + winnings_of_B))
    return solution


def estimate_winning_probability_2(deck_A, deck_B, no_of_iterations=500):
    winnings_of_A = 0
    winnings_of_B = 0
    solution = []

    # if deck_A is invalid returns immediate winning for player B
    if len(deck_A) < 5:
        return [1]

    for _ in range(no_of_iterations):
        hand_A = [deck_A[i] for i in np.random.choice(np.arange(len(deck_A)), 5, replace=False)]
        hand_B = np.random.choice(deck_B, 5, replace=False)
        score_A, score_B = hands_comparison(hand_A, hand_B)
        winnings_of_A += score_A
        winnings_of_B += score_B
        solution.append(winnings_of_B / (winnings_of_A + winnings_of_B))
    return solution


def a():
    deck_A = [(i, j) for i in range(2, 11) for j in range(4)]
    deck_B = [i for i in range(4)] * 4
    iterations = 10 ** 4
    solution_1 = estimate_winning_probability_1(deck_A, deck_B, no_of_iterations=iterations)
    solution_2 = estimate_winning_probability_2(deck_A, deck_B, no_of_iterations=iterations)
    print(solution_1[-1], solution_2[-1])
    plt.plot(np.arange(iterations), solution_1)
    plt.plot(np.arange(iterations), solution_2)
    plt.show()


def b():
    print("Probability of winning with deck A")
    iterations = 10
    # full
    deck_A = [(i, j) for i in range(2, 11) for j in range(4)]
    deck_B = [i for i in range(4)] * 4
    solution = estimate_winning_probability_1(deck_A, deck_B, no_of_iterations=iterations)
    print("Full:", solution[-1])
    # removing one color
    deck_A = [(i, j) for i in range(2, 11) for j in range(3)]
    deck_B = [i for i in range(4)] * 4
    solution = estimate_winning_probability_1(deck_A, deck_B, no_of_iterations=iterations)
    print("With removed one color:", solution[-1])
    # removing two color
    deck_A = [(i, j) for i in range(2, 11) for j in range(2)]
    deck_B = [i for i in range(4)] * 4
    solution = estimate_winning_probability_1(deck_A, deck_B, no_of_iterations=iterations)
    print("With removed two colors:", solution[-1])
    # removing three color
    deck_A = [(i, j) for i in range(2, 11) for j in range(1)]
    deck_B = [i for i in range(4)] * 4
    solution = estimate_winning_probability_1(deck_A, deck_B, no_of_iterations=iterations)
    print("With removed three colors:", solution[-1])

    # removed card from 2 to 5 inclusively
    deck_A = [(i, j) for i in range(6, 11) for j in range(4)]
    deck_B = [i for i in range(4)] * 4
    solution = estimate_winning_probability_1(deck_A, deck_B, no_of_iterations=iterations)
    print("\nWith removed card from 2 to 5 inclusively:", solution[-1])
    # removed card from 2 to 5 inclusively and one color
    deck_A = [(i, j) for i in range(6, 11) for j in range(3)]
    deck_B = [i for i in range(4)] * 4
    solution = estimate_winning_probability_1(deck_A, deck_B, no_of_iterations=iterations)
    print("With removed card from 2 to 5 inclusively and one color:", solution[-1])
    # removed card from 2 to 5 inclusively and two colors
    deck_A = [(i, j) for i in range(6, 11) for j in range(2)]
    deck_B = [i for i in range(4)] * 4
    solution = estimate_winning_probability_1(deck_A, deck_B, no_of_iterations=iterations)
    print("With removed card from 2 to 5 inclusively and two colors:", solution[-1])
    # removed card from 2 to 5 inclusively and three colors
    deck_A = [(i, j) for i in range(6, 11) for j in range(1)]
    deck_B = [i for i in range(4)] * 4
    solution = estimate_winning_probability_1(deck_A, deck_B, no_of_iterations=iterations)
    print("With removed card from 2 to 5 inclusively and three colors:", solution[-1])


def weighted_sum_approach(deck_A, deck_B, population_size=100, max_iter=10 ** 2, alpha=0.1, mode='debug'):
    chromosome_length = len(deck_A)
    population = np.random.randint(2, size=chromosome_length).astype(int)
    for i in np.random.randint(0, chromosome_length, population_size-1):
        individual = np.hstack([np.ones(i), np.zeros(chromosome_length - i)]).astype(int)
        np.random.shuffle(individual)
        population = np.vstack([population, individual])
    F_1 = []
    F_2 = []

    for _ in tqdm(range(max_iter)):
        f_1 = (chromosome_length - np.sum(population, axis=1)) / chromosome_length  # percent of rejected cards
        f_2 = np.array([estimate_winning_probability_1([card for selected, card in zip(individual, deck_A) if selected],
                                                       deck_B)[-1] for individual in population])

        # finding external set
        not_external = []
        for index_of_considered_individual in range(population_size):
            for index_of_compared_individual in range(population_size):
                if index_of_considered_individual not in not_external:
                    if f_1[index_of_compared_individual] < f_1[index_of_considered_individual] and \
                            f_2[index_of_compared_individual] < f_2[index_of_considered_individual]:
                        not_external.append(index_of_considered_individual)
                        break
        external_indexes = np.array([index for index in range(population_size) if index not in not_external])
        external = population[external_indexes]

        # Parent selection
        w_1 = np.random.random()
        w_2 = 1 - w_1

        f = f_1 * w_1 + f_2 * w_2

        f_min = np.min(f)
        f_total = np.sum(f) - f_min * f.shape[0]
        probabilities = (f - f_min) / f_total

        parents = population[np.random.choice(population.shape[0], population_size - external.shape[0], p=probabilities)]

        # crossover
        new_population = external
        for _ in range(int((population_size - external_indexes.shape[0]) / 2)):
            parent_1, parent_2 = parents[np.random.choice(parents.shape[0], 2)]

            # one point crossover
            cutting_point = np.random.randint(0, chromosome_length)
            child_1 = np.hstack([parent_1[:cutting_point], parent_2[cutting_point:]])
            child_2 = np.hstack([parent_2[:cutting_point], parent_1[cutting_point:]])

            new_population = np.vstack([new_population, child_1, child_2])

        if new_population.shape[0] != population_size:
            parent_1, parent_2 = parents[np.random.choice(parents.shape[0], 2)]

            cutting_point = np.random.randint(0, chromosome_length)
            child_1 = np.hstack([parent_1[:cutting_point], parent_2[cutting_point:]])

            new_population = np.vstack([new_population, child_1])

        if new_population.shape[0]!=population.shape[0]:
            print(new_population.shape[0])
            print(population.shape[0])
            print(population_size)
            print("Pop_size error")

        # mutation
        for index in range(population_size):
            if np.random.random()<alpha:
                chosen_bit = np.random.randint(0,chromosome_length)
                new_population[index,chosen_bit] = not new_population[index,chosen_bit]

        population = new_population

        F_1.append(f_1)
        F_2.append(f_2)

    with open("zad3_data.txt", 'w', encoding="UTF-8") as output_file:
        for f_1, f_2 in zip(F_1,F_2):
            output_file.write(''.join(str(num)+" " for num in f_1) + "\n")
            output_file.write(''.join(str(num)+" " for num in f_2) + "\n")

        # # ?
        # if external.shape[0] == population_size:
        #     break
    f_1 = (chromosome_length - np.sum(population, axis=1)) / chromosome_length  # percent of rejected cards
    f_2 = np.array([estimate_winning_probability_1([card for selected, card in zip(individual, deck_A) if selected],
                                                   deck_B)[-1] for individual in population])

    return population,f_1,f_2




if __name__ == "__main__":
    b()
    # with open("Zad3_data.txt",'r',encoding='UTF-8') as input_file, open("Zad3_preprocessed_data.txt",'w',encoding="UTF-8") as output_file:
    #     for i, line in enumerate(input_file):
    #         if i%2==0:
    #             f_1 = np.array([float(num) for num in line.split()])
    #         else:
    #             f_2 = np.array([float(num) for num in line.split()])
    #
    #             not_external = []
    #             for index_of_considered_individual in range(f_1.shape[0]):
    #                 for index_of_compared_individual in range(f_1.shape[0]):
    #                     if index_of_considered_individual not in not_external:
    #                         if f_1[index_of_compared_individual] < f_1[index_of_considered_individual] and \
    #                                 f_2[index_of_compared_individual] < f_2[index_of_considered_individual]:
    #                             not_external.append(index_of_considered_individual)
    #                             break
    #             external_indexes = np.array([index for index in range(f_1.shape[0]) if index not in not_external])
    #             f_1 = f_1[external_indexes]
    #             f_2 = f_2[external_indexes]
    #
    #             if f_1.size > 1:
    #                 output_file.write(''.join(str(num)+" " for num in f_1) + "\n")
    #                 output_file.write(''.join(str(num)+" " for num in f_2) + "\n")



    #
    #
    # with open("Zad3_preprocessed_data.txt",'r',encoding='UTF-8') as input_file:
    #
    #     for i, line in enumerate(input_file):
    #         if i%2==0:
    #             if i==0:
    #                 f_1 = np.array([float(num) for num in line.split()])
    #             f_1 = np.hstack([f_1,np.array([float(num) for num in line.split()])])
    #         else:
    #             if i==1:
    #                 f_2 = np.array([float(num) for num in line.split()])
    #             f_2 = np.hstack([f_2,np.array([float(num) for num in line.split()])])
    #
    # not_external = []
    # for index_of_considered_individual in tqdm(range(f_1.shape[0])):
    #     for index_of_compared_individual in range(f_1.shape[0]):
    #         if index_of_considered_individual not in not_external:
    #             if f_1[index_of_compared_individual] < f_1[index_of_considered_individual] and \
    #                     f_2[index_of_compared_individual] < f_2[index_of_considered_individual]:
    #                 not_external.append(index_of_considered_individual)
    #                 break
    # external_indexes = np.array([index for index in range(f_1.shape[0]) if index not in not_external])
    # f_1 = f_1[external_indexes]
    # f_2 = f_2[external_indexes]
    #
    # plt.scatter(f_1,f_2)
    # plt.xlabel("Percent of rejected cards")
    # plt.ylabel("Loosing probability")
    # plt.title("Pareto front")
    # plt.show()
    # print(f_1)
    # print(f_2)





    # deck_A = [(i, j) for i in range(2, 11) for j in range(4)]
    # deck_B = [i for i in range(4)] * 4
    # # np.random.seed(1)
    # population,f_1,f_2 = weighted_sum_approach(deck_A, deck_B, max_iter=10**2,population_size=10**2)
    # plt.scatter(f_1,f_2)
    # plt.show()
    # print(f_1)
    # print(f_2)
