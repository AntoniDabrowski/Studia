import numpy as np
import matplotlib.pyplot as plt


def calculate_estimators(p,n):

    arr = np.random.binomial(5, p, n)
    p = np.mean(arr)/5
    # print(p)
    density_estimated = 5*np.power(p,4)*(1-p)+np.power(p,5)
    # density_estimated = p
    return density_estimated

def final_calculation(p,n):
    arr = np.array([calculate_estimators(p,n) for _ in range(10000)])
    density_true = 10*np.power(p,3)*np.power(1-p,2)+5*np.power(p,4)*(1-p)+np.power(p,5)
    # density_true = p
    print(np.var(arr),np.mean(np.power(arr-density_true,2)),np.mean(arr)-density_true)
    return [np.var(arr),np.mean(np.power(arr-density_true,2)),np.mean(arr)-density_true]

if __name__ == '__main__':
    print("Wariancja            MSE                  Obciążenie")
    n = 50
    # (a)
    p = 0.1
    d = [final_calculation(p, n)]

    # (b)
    p = 0.3
    d.append(final_calculation(p, n))
    # (c)
    p = 0.5
    d.append(final_calculation(p, n))
    # (d)
    p = 0.7
    d.append(final_calculation(p, n))
    # (e)
    p = 0.9
    d.append(final_calculation(p, n))
    d = np.array(d)
    # plt.bar(np.arange(1,6)-0.2,d[:,0],width=0.2,color='r')
    # plt.bar(np.arange(1,6),d[:,1],width=0.2,color='g')
    # plt.bar(np.arange(1,6)+0.2,d[:,2],width=0.2,color='b')
    # plt.bar(np.arange(1,6)+0.2,-d[:,2],width=0.2,color='b')
    # plt.yscale("log")
    # plt.show()