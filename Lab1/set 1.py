
# es 1
"""
a = int(input("numero 1: "))
b = int(input("numero 2: "))
c = a*b
if c <= 1000:
    print("risultato: ", c)
else:
    c = a+b
    print("risultato: ", c)
"""
# es 2
"""
numRange = range(5, 10, 1)
for i in numRange:
    c = i + i-1
    print(c)
"""
# es 3
"""
listaNum = [1,2,3,4,5]
if listaNum[0] == listaNum[len(listaNum)-1]:
    print("true")
else: print("false")
"""
# es 4
"""
listaNum = [2, 5, 7, 10, 15, 20, 34, 65, 4]
for i in listaNum:
    if i % 5 == 0:
        print(i)
"""
# es 5
"""
testo = "Emma is a good developer. Emma is also a writer"
print(testo.count("Emma"))
"""
# es 6
"""
lista1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lista2 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
lista3 = []
for i in lista1:
    if i % 2 != 0:
        lista3.append(i)
for i in lista2:
    if i % 2 == 0:
        lista3.append(i)
print(lista3)
"""
# es 7
"""
stringa1 = "alea iacta est"
stringa2 = "chittemmuort"
index = int(len(stringa1) / 2)
stringa3 = stringa1[:index] + stringa2 + stringa1[index:]
print(stringa3)
"""
# es 8
"""
stringa1 = "the spice must flow"
stringa2 = "the sleeper has awakened"
stringa3 = stringa1[0] + stringa1[int(len(stringa1)/2)] + stringa1[len(stringa1)-1] + stringa2[0] + stringa2[int(len(stringa2)/2)] + stringa2[len(stringa2)-1]
print(stringa3)
"""
# es 9
"""
stringa = "Advfi 24 DDD %%%a"
upper = sum(c.isupper() for c in stringa)
lower = sum(c.islower() for c in stringa)
digit = sum(c.isdigit() for c in stringa)
special = sum(not c.isalpha() and not c.isdigit() for c in stringa)
print(upper, " ", lower, " ", digit," ", special)
"""
#es 10
"""
riga = "225 asd 225"
totale = 0
numeri = 0
for n in riga:
    if n.isdigit():
        totale += int(n)
        numeri += 1
media = totale/numeri
print(totale, " ", media)
"""