import numpy as np

# Dla każdego potencjalnego ułożenia bloku rozważam liczbę operacji zmiany bitu
# niezbędnych do uzyskania go z ustawienia początkowego. Dla listy długości n
# złożoność czasowa O(n-D).

def opt_dist(L,D):
    L = np.array(L)
    m = np.Inf
    for i in range(len(L)-D+1):
        Sol = np.array([1 if j>=i and j < i+D else 0 for j in range(len(L))])
        m = min(m,np.sum(np.logical_xor(L,Sol)))
    return m


if __name__=="__main__":
    L = [0,0,1,0,0,0,1,0,0,0]
    for i in range(5,-1,-1):
        print(''.join(str(el) for el in L),"i",i,"powinna zwrócić",opt_dist(L,i))