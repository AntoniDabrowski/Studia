import pandas as pd
import numpy as np


if __name__ == '__main__':
    df = pd.DataFrame({"Target":['a','a','a','b','c','b','a'],"Name":[4,5,5,np.NAN,6,5,np.NAN],"sth":[0,0,0,0,0,0,0]})

    attr_df = df[['Name', "Target"]].sort_values('Name')
    targets = attr_df["Target"]
    values = attr_df['Name']
    df['weight'] = np.ones(len(df))
    # Start with a split that puts all the samples into the right subtree
    right_counts = targets.value_counts()
    right_counts['b']+=1

    print(pd.isna(float('nan')))
    
    # attr = "Name"
    # nans = df[df[attr].isna()]
    # nans.loc[:,attr] = df[attr].mean()
    # 
    # new_df = pd.concat([df,nans])
    # print(new_df)

    # nans[attr] = nans[attr].apply(lambda x: df[attr].mean())
    # nans[attr] = pd.DataFrame({attr:np.ones(len(nans))*df[attr].mean()})[attr].values
    # nans.loc[nans[attr] == np.NaN] = df[attr].mean()
    # nans[attr] = nans[attr].map({np.NaN:df[attr].mean()})
    # nans[attr] = .replace(np.NaN,df[attr].mean(),inplace=True)
    # nans[attr] = np.ones(len(nans))*df[attr].mean()
    # nans  = [group_df for val, group_df in df.groupby('Name',dropna=False) if np.isnan(val)]
    # if nans:
    #     nans = nans[0]
    # w = 1 # ???
    # nans['weight'] = nans['weight'].apply(lambda x: x*w)
    # print(pd.concat([df,df]))

    # print(pd.isna(1))
    # print(np.ones(3)*2)
    # for a,b in df.groupby('Name',dropna=False):
    #     print(a)
    #     print(b)
    #     print("\n")
    # print(b.groupby('Target')[1])
    # print(list(d.groupby('Target'))[0])
    # print(list(d.groupby('Target'))[0][1]['weight'].sum())
    # print(list(d.groupby('Target'))[1])


    # print(df)
    # df['weight'] = np.ones(len(df))
    # print(df)
    #
    # l = right_counts.copy()
    # # l['c'] -= 2
    # l = l.drop(labels=['c','b'])
    # print(l)
    # print(right_counts)
    # print(right_counts+l)

