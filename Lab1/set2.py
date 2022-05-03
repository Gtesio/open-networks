#es 1
"""
listOne = [3, 6, 9, 12, 15, 18, 21]
listTwo = [4, 8, 12, 16, 20, 24, 28]
listlen = len(listOne)
listThree = []
for i in range(0, listlen):
    if (i%2) != 0:
        listThree.append(listOne[i])
listlen = len(listTwo)
for i in range(0, listlen):
    if (i%2) == 0:
        listThree.append(listTwo[i])
print(listThree)
"""
# es 2
"""
sampleList = [34, 54, 67, 89, 11, 43, 94]
elem = sampleList[4]
sampleList.remove(sampleList[4])
sampleList.insert(1, elem)
sampleList.append(elem)
print(sampleList)
"""
# es 3
"""
sampleList = [11, 45, 8, 23, 14, 12, 78, 45, 89]
index = int(len(sampleList)/3)
chunk1 = sampleList[:index]
chunk2 = sampleList[index:(index*2)]
chunk3 = sampleList[(index*2):]
print(chunk1," ", chunk2," ", chunk3)
"""
# es 6
"""
firstSet = {23, 42, 65, 57, 78, 83, 29}
secondSet = {57, 83, 29, 67, 73, 43, 48}
inter = firstSet.intersection(secondSet)
for c in inter: firstSet.remove(c)
print(firstSet)
"""