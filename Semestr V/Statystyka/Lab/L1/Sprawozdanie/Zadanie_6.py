import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import cauchy
from time import time
from scipy.stats import logistic


def calculate_estimators(n, theta, sigma):
    assumption = 11
    i = 0
    while np.abs(assumption) > 5:
        sample = cauchy.rvs(loc=theta, scale=sigma, size=n)

        assumption = np.median(sample)
        # assumption = 0
        l = [assumption]
        t_0 = time()

        while np.abs(l_d(assumption, sample)) > 0.00001 and time() - t_0 < 1:
            assumption = assumption - l_d(assumption, sample) / l_dd(assumption, sample)
            l.append(l_d(assumption, sample))

        if np.abs(assumption) > 10:
            i += 1
            print(l)
            print(assumption)
            plt.plot(np.arange(len(l)), np.abs(l))
            plt.show()
            #
            # print(l_d(theta,sample))

            plt.plot(np.arange(0, 10, 0.1), [l_d(t, sample) for t in np.arange(0, 10, 0.1)])
            plt.scatter([np.median(sample)], [l_d(np.median(sample), sample)], color="g")
            plt.plot(np.linspace(0, 10, 100),
                     np.linspace(0, 10, 100) * l_dd(np.median(sample), sample) + l_d(np.median(sample), sample))
            plt.show()
            plt.hist(sample, bins=50, density=True, histtype='step')
            plt.show()
    if i != 0:
        print(i)
    return assumption


def run_experiment(number_of_experiments, n, theta, sigma):
    data = np.array([calculate_estimators(n, theta, sigma) for _ in range(number_of_experiments)])
    print("Wariancja            MSE                  Obciążenie")
    print(np.var(data), np.mean(np.power(data - theta, 2)), np.abs(np.mean(data) - theta))


def l_d(theta, sample, sigma=1):
    return np.sum((sample - theta) / (np.power(sigma, 2) + np.power(sample - theta, 2)))


def l_dd(theta, sample, sigma=1):
    arr_1 = np.power(sample - theta, 2)
    return np.sum((4 * arr_1) / np.power(arr_1 + np.power(sigma, 2), 2) - 2 / (arr_1 + np.power(sigma, 2)))


if __name__ == '__main__':
    # (a)
    # n = 100
    # theta = 1
    # sigma = 1

    # calculate_estimators(n,theta,sigma)
    # (b)
    n = 20
    theta = 4
    sigma = 1
    # # (c)
    # n = 50
    # theta = 1
    # sigma = 2

    run_experiment(10000, n, theta, sigma)
