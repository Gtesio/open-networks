import math

BERt = 1e-3  # BitErrorRate
Rs = 32e9  # symbol rate
Bn = 12.5e9  # noise bandwidth
G_dB = 16  # for use with amplifiers
G = 39.8107
NF_dB = 3  # for use with amplifiers
NF = 1.99526
Planck = 6.62607015e-34
Freq = 193.414e12
Adb = 0.2e-3  # dB/m
b2 = 2.13e-26  # 0.6e-26  # (m Hz^2)^-1
gamma = 1.27e-3   # (mW)^-1
df = 50e9
Alpha = Adb/(10*math.log(math.e, 10))
Leff = 1/Alpha
# Alpha = Adb/(10*log(e, 10)), Leff = 1/alpha


def dbtolin(dbnum):
    return pow(10, dbnum/10)


def lintodb(linnum):
    return 10 * math.log(linnum, 10)
