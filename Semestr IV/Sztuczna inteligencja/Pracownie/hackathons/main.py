import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




if __name__ == '__main__':
    df = pd.read_excel(r'Square_Games_Dataset.xlsx')
    print(df)
    # print(df['item_price [USD]'].tolist())
    # print(df['item_type'].tolist())
    # p = []
    # t = []
    # for price, type in zip(df['item_price [USD]'].tolist(),df['item_type'].tolist()):
    #     p.append(price)
    #     t.append(type=='functional')
    # plt.scatter(p,t)
    # plt.show()