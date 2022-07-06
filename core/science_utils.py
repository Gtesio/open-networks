import math

BERt = 10e-3  # BitErrorRate
Rs = 32e9  # symbol rate
Bn = 12.5e9  # noise bandwidth


def dbtolin(dbnum):
    return pow(10, dbnum/10)


def lintodb(linnum):
    return 10 * math.log(linnum)
