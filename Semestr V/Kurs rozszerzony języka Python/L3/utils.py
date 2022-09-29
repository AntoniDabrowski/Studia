import matplotlib.pyplot as plt
import numpy as np
from time import time
from tqdm.auto import tqdm

"""
Functions below are used just to present results,
I won't write detailed specification to them.  
"""


def test(function, inputs):
    # For each input measure a time of running the function.
    data = np.zeros(inputs.shape)
    for i, n in enumerate(tqdm(inputs)):
        t_0 = time()
        function(n)
        t_1 = time()
        data[i] = t_1 - t_0
    print(repr(data))
    return data


def plot_results(functions, function_names, inputs, title):
    for func, func_name in zip(functions, function_names):
        plt.plot(inputs, test(func, inputs), label=func_name)
    plt.xscale("log")
    plt.title(title)
    plt.legend()
    plt.show()
