import numpy as np
from scipy.stats import norm, cauchy, t
import matplotlib.pyplot as plt


if __name__ == '__main__':
    n = 1000
    arr_1 = np.random.normal(13,0,n)
    arr_2 = np.random.normal(2,1,n)
    plt.hist(arr_1)
    # plt.hist(arr_1-arr_2)
    plt.show()