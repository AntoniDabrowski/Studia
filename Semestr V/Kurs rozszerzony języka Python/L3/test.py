import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    n = 1000
    X = np.random.randn(n)
    Y = np.random.randn(n)
    Z = np.random.randn(n)
    norm = np.sqrt(np.power(X,2)+np.power(Y,2)+np.power(Z,2))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs=X/norm, ys=Y/norm, zs=Z/norm)
    plt.show()