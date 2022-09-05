import numpy as np
from scipy.special import factorial
import matplotlib.pyplot as plt

def calculate_estimators(n,lam,m):

    arr = np.random.poisson(lam, n)
    lam = np.mean(arr)
    density_estimated = np.array([[pmf(x,lam) for x in range(m)]]).T
    return density_estimated

def pmf(x,lam):
    return np.power(lam,x)*np.exp(-lam)/factorial(x)

def final_calculation(n,lam,m=11):
    arr = np.hstack([calculate_estimators(n,lam,m) for _ in range(10000)])
    density_true = pmf(np.arange(m),lam)
    print("Wariancja            MSE                  Obciążenie")
    D = []
    for true_val, row in zip(density_true,arr):
        D.append([np.var(row), np.mean(np.power(row - true_val, 2)), np.mean(row) - true_val])
        print(np.var(row), np.mean(np.power(row - true_val, 2)), np.mean(row) - true_val)
    return D

def plot_results(D,m=11):
    plt.bar(np.arange(m)+0.2,D[:,0], width=0.2,color='r',label="Wariancja")
    plt.bar(np.arange(m),D[:,1], width=0.2,color='g',label="MSE")
    plt.bar(np.arange(m)-0.2,D[:,2], width=0.2,color='b',label="Obciążenie")
    neg = D[:,2]<0
    plt.bar(np.arange(m)[neg]-0.2,-D[:,2][neg], width=0.2,color='cyan',label="- Obciążenie")
    # plt.yscale('symlog')
    plt.yscale('log')
    plt.legend()
    plt.title("n = "+str(n)+", lambda = "+str(lam))
    plt.xlabel("x")
    plt.ylabel("Wartości")
    plt.show()

if __name__ == '__main__':
    n = 100
    m = 20
    # (a)
    # lam = 0.5
    # D = np.array(final_calculation(n,lam))
    # plot_results(D)
    # (b)
    # lam = 1
    # D = np.array(final_calculation(n,lam))
    # plot_results(D)
    # (c)
    # lam = 2
    # D = np.array(final_calculation(n,lam))
    # plot_results(D)
    # (d)
    lam = 5
    D = np.array(final_calculation(n,lam,m))
    plot_results(D,m)