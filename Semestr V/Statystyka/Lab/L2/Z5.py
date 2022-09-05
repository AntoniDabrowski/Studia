import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def calculate_estimators(n,theta,sigma):

    arr = np.random.laplace(theta,sigma,n)


    e1 = np.mean(arr)

    e2 = np.median(arr)

    w = np.random.randint(1,100,n)
    w = w/np.sum(w)
    e3 = np.sum(w*arr)

    w = norm.pdf(norm.ppf(np.arange(n)/n)) - norm.pdf(norm.ppf(np.arange(1,n+1)/n))
    e4 = np.sum(w*np.sort(arr))

    return np.array([[e1], [e2], [e3], [e4]])

def generate_data(n,theta,sigma):
    data = np.array(calculate_estimators(n,theta,sigma))
    for _ in range(10000-1):
        data = np.hstack([data,calculate_estimators(n,theta,sigma)])
    e1 = data[0, :]
    e2 = data[1, :]
    e3 = data[2, :]
    e4 = data[3, :]
    return e1, e2, e3, e4

def final_calculation(n,theat,sigma):
    e1, e2, e3, e4 = generate_data(n,theat,sigma)
    print("Wariancja            MSE                  Obciążenie")
    print(np.var(e1),np.mean(np.power(e1-theta,2)),np.abs(np.mean(e1)-theta))
    print(np.var(e2),np.mean(np.power(e2-theta,2)),np.abs(np.mean(e2)-theta))
    print(np.var(e3),np.mean(np.power(e3-theta,2)),np.abs(np.mean(e3)-theta))
    print(np.var(e4),np.mean(np.power(e4-theta,2)),np.abs(np.mean(e4)-theta))

if __name__ == '__main__':
    n = 100
    # (a)
    # theta = 1
    # sigma = 1
    # final_calculation(n,theta,sigma)
    # (b)
    # theta = 4
    # sigma = 1
    # final_calculation(n,theta,sigma)
    # (c)
    theta = 1
    sigma = 2

    final_calculation(n,theta,sigma)