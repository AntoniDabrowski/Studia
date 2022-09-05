import numpy as np

def tri(n,modulo):
    m = np.zeros((n+2,n+2)).astype(int)
    m[1,1]=1
    for i in range(2,n+1):
        for j in range(i+1):
            m[i,j]=(m[i-1,j]+m[i-1,j-1])%modulo
    return m[1:,1:]

def mod_inv(x,p):
    return pow(x,p-2,p)

if __name__ == '__main__':
    # s = set()
    # current_sum = 1
    # for i in range(1,100):
    #     current_sum *= i
    #     current_sum %= 127
    #     s.add(current_sum)
    #     print(current_sum)
    # print(list(s))
    p = 127
    l = []
    for i in range(1,(p//2)+1):
        l.append(pow(i,-1,p))
    print(len(sorted([el for el in l if el<(p//2)+1])))