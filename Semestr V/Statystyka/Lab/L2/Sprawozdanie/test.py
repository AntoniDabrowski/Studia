import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import cauchy

if __name__ == '__main__':
    l = """0.07914722034951074 0.07917998010327139 0.005723613697712571
0.04615325645367008 0.046188224694526846 0.0059133950364219645
0.10535379677013536 0.10539758038473633 0.006616918814747463
0.08212816238834832 3.045262914186622 1.721375831071842"""
    for line in l.split("\n"):
        t = ""
        for word in line.split():
            t+=word[:10]+" & "
        print(t[:-2])
