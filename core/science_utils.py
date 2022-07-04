import math


def dbtolin(dbnum):
    return pow(10, dbnum/10)


def lintodb(linnum):
    return 10 * math.log(linnum)
