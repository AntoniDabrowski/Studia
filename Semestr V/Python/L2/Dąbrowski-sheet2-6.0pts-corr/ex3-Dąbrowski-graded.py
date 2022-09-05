from time import time

def sudan_Memoization(n,x,y):
    # specification: function calculate Sudan function using memoization
    # input type: int, int, int; all greater or equal 0
    # output type: int
    def F(n,x,y,d):
        if (n,x,y) in d:
            return d[(n,x,y)]
        if n == 0:
            d[(n,x,y)] = x+y
            return x+y
        if y == 0:
            d[(n,x,y)] = x
            return x
        d[(n,x,y)] = F(n-1,F(n,x,y-1,d),F(n,x,y-1,d)+y,d)
        return d[(n,x,y)]
    d = dict()
    return F(n,x,y,d)
"""
For n = 0 I checked all combinations of y and x from 0 up to 10^6 and all were computed instantly
For n = 1 I found that increasing x doesn't really affect computation time, however upper bound
for parameter y is 996, where my recursive algorithm reach a maximum recursion depth
For n = 2 maximum recursion depth is achieved at y = 3, upper bound is y = 2, x = 5
"""

def sudan_simple(n,x,y):
    # specification: function calculate Sudan function
    # input type: int, int, int; all greater or equal 0
    # output type: int
    if n == 0:
        return x+y
    if y == 0:
        return x
    return sudan_simple(n-1,sudan_simple(n,x,y-1),sudan_simple(n,x,y-1)+y)
"""
For n = 1 highest computed value is for x = 111, and y = 25, takes about 10s
For n = 2 highest computed value is for x = 1, and y = 2
"""


if __name__ == '__main__':
    # n=1
    # for y in range(1000):
    #     l = ""
    #     for x  in range(1000):
    #         l += str(sudan(n,x,y)) + " "
    #     print(l)
    t_0 = time()
    sudan_Memoization(2,5,2)
    print("sudan_Memoization: ",time()-t_0)

    t_0 = time()
    print(sudan_simple(1,111,25))
    print("sudan_simple: ",time()-t_0)

    # Grade: 2.0
    # Didactic notes: Good job! I overall like the balance of comments, docstrings and so on.