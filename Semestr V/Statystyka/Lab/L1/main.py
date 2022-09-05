import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    Y = np.array([0.00000000e+00, 0.00000000e+00, 1.03497505e-03, 2.98810005e-03,
       9.57727432e-03, 4.19754982e-02, 1.63973808e-01, 6.51125669e-01,
       2.58593011e+00, 1.05450807e+01, 4.70223539e+01, 1.94918445e+02,
       8.06097040e+02, 3.34312502e+03, 3.14168227e+04])
    X = np.logspace(2, 6.5, 15, endpoint=True).astype(int)
    plt.plot(X,Y)
    # plt.yscale("log")
    plt.xscale("log")
    plt.show()