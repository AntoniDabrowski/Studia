import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import cauchy
from time import time
from scipy.stats import logistic

def calculate_estimators(n,theta,sigma):

    sample = cauchy.rvs(loc=theta, scale=sigma, size=n)

    assumption = np.median(sample)
    l = [assumption]
    t_0 = time()

    while np.abs(l_d(assumption,sample))>0.00001 and time()-t_0<1:
        assumption = assumption - l_d(assumption, sample) / l_dd(assumption, sample)
        l.append(l_d(assumption, sample))
    # if assumption>5:
    #     print(assumption)
    return assumption


def run_experiment(number_of_experiments,n,theta,sigma):
    data = np.array([calculate_estimators(n,theta,sigma) for _ in range(number_of_experiments)])
    print(np.mean(data))
    print(np.median(data))
    plt.hist(np.sort(data)[50:9950],bins=100)
    plt.title("n=20,θ=4,σ=1, dane okrojone (centralne 99,5%)")
    plt.show()




def l_d(theta,sample,sigma=1):
    return np.sum((sample-theta)/(np.power(sigma,2)+np.power(sample-theta,2)))

def l_dd(theta,sample,sigma=1):
    arr_1 = np.power(sample-theta,2)
    return np.sum((4*arr_1)/np.power(arr_1+np.power(sigma,2),2) - 2/(arr_1+np.power(sigma,2)))

if __name__ == '__main__':
    # (a)
    n = 20
    # theta = 1
    # sigma = 1

    # calculate_estimators(n,theta,sigma)
    # (b)
    # n = 50
    theta = 4
    sigma = 1
    # # (c)
    # n = 50
    # theta = 1
    # sigma = 2

    run_experiment(10000,n,theta,sigma)