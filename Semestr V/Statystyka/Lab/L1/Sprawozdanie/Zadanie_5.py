import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import logistic

def calculate_estimators(n,theta,sigma):


    sample = np.random.logistic(theta,sigma, n)

    assumption = np.mean(sample)
    # assumption = 0
    # l = [assumption]
    while np.abs(l_d(assumption,sample))>0.001:
        assumption = assumption - l_d(assumption, sample) / l_dd(assumption, sample)
        # l.append(l_d(assumption, sample))
    return assumption


    # print(l)
    # plt.scatter(np.arange(len(l)),l)
    # plt.show()
    #
    # print(l_d(theta,sample))
    # plt.scatter(np.arange(0,10,0.1),[l_d(t,sample) for t in np.arange(0,10,0.1)])
    # plt.show()
    # plt.hist(sample,bins=50,density=True,histtype='step')
    # plt.show()

def run_experiment(number_of_experiments,n,theta,sigma):
    data = np.array([calculate_estimators(n,theta,sigma) for _ in range(number_of_experiments)])

    # print("Wariancja            MSE                  Obciążenie")
    print(np.var(data),np.mean(np.power(data-theta,2)),np.abs(np.mean(data)-theta))





def l_d(theta,sample):
    return sample.shape[0]-2*np.sum(np.exp(-(sample-theta))/(1+np.exp(-(sample-theta))))

def l_dd(theta,sample):
    return -2*np.sum(np.exp(-(sample-theta))/np.power(1+np.exp(-(sample-theta)),2))


if __name__ == '__main__':
    # (a)
    n = 100
    theta = 1
    sigma = 1

    run_experiment(10000,n,theta,sigma)
    # calculate_estimators(n,theta,sigma)
    # (b)
    theta = 4
    sigma = 1
    run_experiment(10000,n,theta,sigma)
    # # (c)
    theta = 1
    sigma = 2

    run_experiment(10000,n,theta,sigma)