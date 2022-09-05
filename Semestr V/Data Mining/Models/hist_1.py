import matplotlib.pyplot as plt



if __name__=="__main__":
    labels1 = ["MLP","Autoencoder","CNNs","RNNs","RBM","NADE","Neural Attention","Adversary Network","DRL","Hybrid Models"]
    data1 = [22,26,25,28,7,3,15,4,7,11]
    labels2 = ["Sequential\nInformation","Text","Images","Audio","Video","Networks","Others"]
    data2 = [32,23,16,4,4,9,11]
    plt.bar(x=labels2,height=data2)
    plt.xticks(rotation = 45)
    plt.show()