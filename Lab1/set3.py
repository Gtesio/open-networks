import numpy as np
# es 2
#a = np.arange(100, 200, 10).reshape(5, 2)
#print(a)
# es 3
"""
a = np.array([11, 22, 33, 44, 55, 66, 77, 88, 99]).reshape(3, 3)
b = a[:, -1]
print(b)
"""
# es 4
"""
a = np.array([3 ,6, 9, 12, 15 ,18, 21, 24, 27 ,30, 33, 36, 39 ,42, 45, 48, 51 ,54, 57, 60]).reshape(5, 4)
print(a)
b = a[::2, 1::2]
print(b)
"""
# es 5
"""
a = np.array([5, 6, 9, 21, 18, 27]).reshape(2, 3)
b = np.array([15, 33, 24, 4, 7, 1]).reshape(2, 3)
c = np.add(a, b)
d = []
for i in c:
    d.append(np.sqrt(i))
d = np.array(d).reshape(2, 3)
print(c)
print(d)
"""
#es6
"""
a = np.array([34, 43, 73, 82, 22, 12, 53, 94, 66]).reshape(3,3)
a.sort()
print(a)
"""
# es 7
"""
a = np.array([34, 43, 73, 82, 22, 12, 53, 94, 66]).reshape(3,3)
print(np.amax(a[0]), " ", np.amin(a[1]))
"""
# es 8
"""
a = np.array([34, 43, 73, 82, 22, 12, 53, 94, 66]).reshape(3,3)
b = np.array([10, 10, 10])
print(a)
a = np.delete(a, 1, 1)
print(a)
a = np.insert(a, 1, b, 1)
print(a)
"""