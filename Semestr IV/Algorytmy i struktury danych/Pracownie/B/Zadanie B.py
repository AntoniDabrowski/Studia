import numpy as np
from tqdm import tqdm


def brute_force(A):
    def base10toN(num, base):
        converted_string, modstring = "", ""
        currentnum = num
        if not 1 < base < 37:
            raise ValueError("base must be between 2 and 36")
        if not num:
            return '0'
        while currentnum:
            mod = currentnum % base
            currentnum = currentnum // base
            converted_string = chr(48 + mod + 7 * (mod > 10)) + converted_string
        return converted_string

    def normalize(word, wanted_length):
        return "0" * (wanted_length - len(word)) + word

    highest_tower = 0
    lowest_dist = np.Inf
    for partition in tqdm(range(3 ** A.shape[0])):
        partition = normalize(base10toN(partition, 3), len(A))
        first_subset = np.array([element == '0' for element in partition])
        second_subset = np.array([element == '1' for element in partition])
        first_sum = np.sum(A[first_subset])
        second_sum = np.sum(A[second_subset])
        if first_sum and second_sum and np.abs(first_sum - second_sum) <= lowest_dist:
            lowest_dist = np.abs(first_sum - second_sum)
            if lowest_dist == 0 and first_sum > highest_tower:
                highest_tower = first_sum
    if lowest_dist == 0:
        return "TAK", highest_tower
    else:
        return "NIE", lowest_dist


def test_generator(low, high, n):
    return np.random.choice(np.arange(high - low) + low, n, replace=False)


def alg(A):
    s = np.sum(A)
    s_2 = s // 2 + 1
    arr = np.zeros(s_2).astype(bool)
    arr[0] = True
    for element in A:
        for i in range(s_2 - element):
            arr[i + element] = arr[i] or arr[i + element]
    arr_num = np.array([l for l in range(s_2) if arr[l]])
    min_dist = np.min(np.abs(arr_num - np.vstack([arr_num[1:], np.array([np.Inf])])))
    return arr_num, min_dist


def check(L, current_element, new_element, super_nodes):
    def reconstruct_path(current_sum):
        path = []
        while current_sum not in super_nodes:
            path.append(L[current_sum])
            current_sum -= L[current_sum]
        return path

    existing_path = reconstruct_path(current_element)
    new_path = reconstruct_path(current_element - new_element)
    is_good = True
    for element in existing_path:
        if element in new_path:
            is_good = False
    return is_good


def new_alg(A):
    # A = np.sort(A)
    L = [0 for _ in range(sum(A) + 1)]
    # min_dist = np.min((A - np.hstack([0, A[:-1]]))[1:])
    super_nodes = [0]
    max_num = 0
    for a in A:
        temp = 0
        temp_super_nodes = []
        for i in range(min(max_num + 1, len(L) - a)):
            if (L[i] and L[i] != [a]) or i == 0:
                if L[i + a] and i+a not in super_nodes:
                    if check(L, i + a, a, super_nodes):
                        # L[i + a] = a
                        temp = max(temp, i + a)
                        temp_super_nodes.append(i + a)
                else:
                    L[i + a] = a
                    temp = max(temp, i + a)
        max_num = max(max_num, temp)
        super_nodes += temp_super_nodes
    # print(repr(L[:int(sum(L)/2)]))
    print(repr([i for i in super_nodes if i < sum(L) / 2]))
    # for i, l in enumerate(L):
    #     if i < len(L) / 2:
    #         print(i, l)
    # if len(l)>1:
    #     return i
    # previous = np.inf
    # best_solution = 0
    # for i in range(len(L)-1,0,-1):
    #     if i <= best_solution:
    #         return "TAK", best_solution
    #     if len(L[i])>1:
    #         list_of_similar_elements = check(L,i)
    #         if list_of_similar_elements:
    #             best_solution = max(best_solution,i) # probably max is not necessary
    #         else:
    #             return "TAK", i
    #     elif L[i]:
    #         min_dist = min(min_dist,previous)
    #         previous = i
    # return "NIE", min_dist


def third_approach(given_list):
    L = sorted(given_list, reverse=True)
    A = [[] for _ in range(len(L))]
    B = [[] for _ in range(len(L))]
    A[0] = [L[0]]
    A[1] = [L[0]]
    B[1] = [L[1]]
    opt_dist = [np.inf for _ in range(len(L))]
    opt_dist[0] = L[0]
    opt_dist[1] = np.abs(L[0] - L[1])
    max_hight = [0 for _ in range(len(L))]
    if L[0] == L[1]:
        max_hight[1] = L[0]
    for i in range(2, len(L)):
        lowest_diff = opt_dist[0] - L[i]
        A[i] = A[0]
        B[i] = [L[i]]
        for j in range(i - 1, -1, -1):
            if opt_dist[j] != np.inf:
                current_dist = np.abs(opt_dist[j] - L[i])
                if current_dist == 0:
                    A[i] = A[j]
                    B[i] = B[j] + [L[i]]
                    max_hight[i] = sum(A[i])
                    break
                if current_dist < lowest_diff:
                    lowest_diff = current_dist
                    if sum(B[j]) + L[i] < sum(A[j]):
                        A[i] = A[j]
                        B[i] = B[j] + [L[i]]
                    else:
                        A[i] = B[j] + [L[i]]
                        B[i] = A[j]
        # if max_hight[i] != 0:
        opt_dist[i] = lowest_diff
    # print("A  B  opt_dist  max_hight")
    # for i in range(len(L)):
    #     print(A[i],B[i],opt_dist[i],max_hight[i])
    print(max(max_hight))

def alg6(L):
    reachable = np.zeros((sum(L) // 2)+1).astype(bool)
    solutions = []
    max_size = sum(L) // 2
    reachable[0] = True
    max_num = 0
    for num in L:
        added_to_solutions = False
        for i in range(min(max_size, max_num)+1):
            if i + num <= max_size and reachable[i]:
                if reachable[i + num]:
                    solutions.append(i + num)
                    added_to_solutions = True
                else:
                    reachable[i + num] = True
        max_num = max_num + num
    # print(reachable)
    return sorted(list(set(solutions)))




def alg7(A):
    def check_temp_super_node(L, num, temp_super_nodes):
        is_good = True
        for node in temp_super_nodes:
            if node - num > 0 and (node - num) in L:
                is_good = False
        return is_good

    # A = np.sort(A)
    L = [0 for _ in range(sum(A) + 1)]
    # min_dist = np.min((A - np.hstack([0, A[:-1]]))[1:])
    super_nodes = [0]
    max_num = 0
    for a in A:
        temp = 0
        temp_super_nodes = []
        for i in range(min(max_num + 1, len(L) - a)):
            if (L[i] and L[i] != [a]) or i == 0:
                if L[i + a] and i+a not in super_nodes and check_temp_super_node(L,a,temp_super_nodes):
                    # L[i + a] = a
                    temp = max(temp, i + a)
                    temp_super_nodes.append(i + a)
                else:
                    L[i + a] = a
                    temp = max(temp, i + a)
        max_num = max(max_num, temp)
        super_nodes += temp_super_nodes
    print(repr(L[:int(sum(L)/2)]))
    print(repr(sorted([i for i in super_nodes if i < sum(L) / 2])))

if __name__ == '__main__':
    # A = np.array([2, 3, 5, 7, 9,18])
    np.random.seed(6)
    # A = np.array(sorted(test_generator(100, 500, 10)))
    # A = sorted([16,  4,  6, 16, 16, 18, 14])
    # A = np.array([5, 7, 10, 11, 17, 20, 21, 27, 28, 29, 33, 37])
    # A = np.array([2,3,5,7,11,13,17])
    # while new_alg(A)==brute_force(A)[1]:
    #     A = np.array(sorted(test_generator(2,20,7)))
    # print(repr(A))
    A = np.array(sorted([10,15,22,75,117]))
    # print(alg7(A))
    # third_approach(A)
    print(brute_force(A))
    # print(alg6(A))
    print(sum(A)//2)
    # print(repr(A))
    # print(sorted(A))
    # print(alg(A))
    # print(brute_force(A))
