import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == '__main__':
    df = pd.read_excel("data.xlsx")
    eng = df['ENG'].to_numpy()
    rejon = df['REJON'].tolist()
    pole = df['POLE'].tolist()

    # r = {name:[] for name in list(set(rejon))}

    # for name, eng_single in zip(rejon,eng):
    #     r[name].append(eng_single)
    # for key in list(r.keys()):
    #     plt.plot(r[key])
    # plt.show()

    # plt.hist(sorted(eng)[::-1],bins=9)
    # plt.yscale('log')
    # plt.show()

    sns.lineplot(data=df, hue='POLE', x='DATA', y='ENG')
    # r = {name:[] for name in list(set(pole))}
    # for pole_single, eng_single in zip(pole,eng):
    #     r[pole_single].append(eng_single)
    # for key in list(r.keys()):
    #     plt.plot(r[key])
    # plt.show()
