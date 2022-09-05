import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import statsmodels.api as sm
import pylab as py



def estimate_theta(theta,n):
    arr = np.random.beta(theta, 1, n)
    theta = -n/np.sum(np.log(arr))
    return theta

def estimate_fisher_information(theta,n):
    new_theta = estimate_theta(theta,n)
    fi = 1 / np.power(new_theta,2)
    return fi

def final_calculation(theta,n,fi):
    arr = np.array([estimate_theta(theta,n) for _ in range(10000)])
    Y = np.sqrt(n*fi)*(arr - theta)
    plt.hist(Y,bins=40)
    plt.show()
    sm.qqplot(Y, line='45')
    py.show()

if __name__ == '__main__':
    n = 10000
    # (a)
    theta = 0.5
    fi = np.mean(np.array([estimate_fisher_information(theta,n) for _ in range(10000)]))
    final_calculation(theta,n,fi)
    # (b)
    theta = 1
    fi = np.mean(np.array([estimate_fisher_information(theta,n) for _ in range(10000)]))
    final_calculation(theta,n,fi)
    # (c)
    theta = 2
    fi = np.mean(np.array([estimate_fisher_information(theta,n) for _ in range(10000)]))
    final_calculation(theta, n, fi)
    # (d)
    theta = 5
    fi = np.mean(np.array([estimate_fisher_information(theta,n) for _ in range(10000)]))
    final_calculation(theta, n, fi)