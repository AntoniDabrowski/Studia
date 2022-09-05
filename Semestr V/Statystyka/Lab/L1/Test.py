import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import cauchy

if __name__ == '__main__':
    l = """0.03997862971923596 0.03997962536754666 0.000997821783034758
0.06149059073133462 0.06149736846847782 0.0026034087545367957
0.05275265081492022 0.052753249102963716 0.0007734908166801002
0.019911046816684888 0.9586093353598187 0.9688644324894651"""
    for line in l.split("\n"):
        t = ""
        for word in line.split():
            t+=word[:10]+" & "
        print(t)