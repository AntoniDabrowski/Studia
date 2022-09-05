from itertools import combinations


s = {"a","b","c"}
s_2 = {"d","a","b","c"}
print(s==s_2)
# s = list(s)
# valuations = {}
# for i in range(1,len(s)+1):
#     for combination in combinations(s,i):
#         valuations[combination] = [True]*i
# print(valuations)