import numpy as np


def alg(L):
    max_sum = np.sum(L)
    arr = np.zeros([2,max_sum + 1]).astype(int)
    arr[0][0] = 0
    max_dist = 0
    current = 1
    for element in L:
        temp_dist = 0
        for i in range(max_dist + element+1):
            if (i + element <= max_sum and arr[(current-1)%2][i + element] != 0) or i==0:
                arr[current][i] = max(arr[current][i], arr[(current - 1) % 2][i], arr[(current - 1) % 2][i + element])
                temp_dist = max(temp_dist, i) # not have to
            if (i - element > 0 and arr[(current-1)%2][i - element] != 0) or i-element==0:
                arr[current][i] = max(arr[current][i],arr[(current-1)%2][i],arr[(current-1)%2][i - element]+element)
                temp_dist = max(temp_dist, i)
            if i - element < 0 and arr[(current-1)%2][np.abs(i-element)]!=0:
                arr[current][i] = max(arr[current][i],arr[(current-1)%2][i],arr[(current-1)%2][np.abs(i-element)]-np.abs(i-element)+element)
                temp_dist = max(temp_dist, i)
            else:
                arr[current][i] = max(arr[current][i],arr[(current-1)%2][i])
        max_dist = max(max_dist, temp_dist)
        current = (current - 1) % 2
    current = (current - 1) % 2
    if arr[current][0]!=0:
        return "TAK",arr[current][0]
    return "NIE",[i for i, l in enumerate(arr[current]) if l>0][0]


if __name__ == '__main__':
    L = np.array(sorted([10, 15, 22, 75, 117]))
    print(alg(L))
