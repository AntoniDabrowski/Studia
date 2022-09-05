import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    X = np.arange(15)+2
    Y = np.array([7.79,7.29,6.98,6.67,6.36,6.05,5.75,5.72,5.69,5.66,5.63,5.60,5.57,5.54,5.51])
    plt.plot(X,Y)
    plt.show()