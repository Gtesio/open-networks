import math

from scipy.special import erfcinv

import elements as el
import random
import matplotlib.pyplot as plt

from core.science_utils import dbtolin, BERt, Rs, Bn

net = el.Network("../resources/nodes.json")
net.connect()

'''
print(pow(10, 20/10))
print(dbtolin(net.getweightedpath().loc["A->C->D->E->F->B", 'SNR']))
print(10 * pow(erfcinv((3/2) * BERt), 2) * (Rs / Bn))
print(2*Rs*math.log(1 + dbtolin(20)*(Rs/Bn), 2)*1e-9)
'''

#  lab6 es 2 plot on same figure bit rate curve vs GSNR in dB of each tech
'''
dB = list(range(1, 51))
fixedrate = []
flexrate = []
shannonrate = []
fixed = 2*pow(erfcinv(2*BERt), 2)*(Rs/Bn)
flex0 = fixed
flex100 = (14/3)*pow(erfcinv((3/2)*BERt), 2)*(Rs/Bn)
flex200 = 10*pow(erfcinv((8/3)*BERt), 2)*(Rs/Bn)

for i in dB:
    gsnr = dbtolin(i)
    if gsnr >= fixed:
        fixedrate.append(100)
    else:
        fixedrate.append(0)
    if gsnr < flex0:
        flexrate.append(0)
    if flex0 <= gsnr < flex100:
        flexrate.append(100)
    if flex100 <= gsnr < flex200:
        flexrate.append(200)
    if gsnr >= flex200:
        flexrate.append(400)
    shannonrate.append(2 * Rs * math.log2(1 + gsnr*(Rs/Bn))*1e-9)

plt.plot(dB, fixedrate, "k", label='fixed rate', linewidth=2)
plt.plot(dB, flexrate, "g", label="flexible rate", linewidth=2)
plt.plot(dB, shannonrate, "b", label="shannon rate", linewidth=2)
plt.legend(loc='upper left')
plt.grid()
plt.title("Possible bitrates for each SNR")
plt.xlabel("dB")
plt.ylabel("Gbps")
plt.show()

'''
conn = []
nodeletters = net.getnodes()
while len(conn) < 100:
    start = random.choice(nodeletters)
    end = random.choice(nodeletters)
    if start != end:
        conn.append(el.Connection(start, end, 1e-3))

'''
net.stream(conn, 'latency')
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.grid()
ax1.set_ylabel("seconds")
ax1.set_title("latency towards each node")
for c in conn:
    if c.getsnr() is None:
        ax1.plot(c.getoutput(), 0, marker='x', color='r')
    else:
        ax1.plot(c.getoutput(), c.getlat(), marker='o', color='b', markersize=3)

ax1.set_ylim(0, 0.005)

net.stream(conn, 'snr')

ax2.grid()
ax2.set_ylabel("dB")
ax2.set_title("snr towards each node")
for c in conn:
    if c.getsnr() is None:
        ax2.plot(c.getoutput(), 0, marker='x', color='r')
    else:
        ax2.plot(c.getoutput(), c.getsnr(), marker='o', color='b', markersize=3)
ax2.set_ylim(0, 100)
'''

# es 5 lab 6, histogram plot of average bit rates and total allocated capacity comparison for 3 transceiver tech
fig2, (at1, at2) = plt.subplots(1, 2)
at1.grid(axis="y")  # average bitrate
at1.set_title("average bitrate")
at2.grid(axis="y")  # total capacity
at2.set_title("total capacity")
at1.set_ylabel("Gbps")
at2.set_ylabel("Gbps")

net.stream(conn)  # fixed rate
total_cap = 0
average_br = 0
xlabels = ["fixed-rate", "flex-rate", "shannon-rate"]
xvalues = []
xcap = []
for c in conn:
    total_cap += c.getbitrate()

xvalues.append(total_cap/len(conn))
xcap.append(total_cap)

net = el.Network("../resources/nodesflex.json")  # flexrate
net.connect()
net.stream(conn)
total_cap = 0
average_br = 0
for c in conn:
    total_cap += c.getbitrate()
xvalues.append(total_cap/len(conn))
xcap.append(total_cap)

net = el.Network("../resources/nodesshannon.json")  # shannon rate
net.connect()
net.stream(conn)
total_cap = 0
average_br = 0
for c in conn:
    total_cap += c.getbitrate()
xvalues.append(total_cap/len(conn))
xcap.append(total_cap)

at1.bar(xlabels, xvalues)
at2.bar(xlabels, xcap)

plt.tight_layout()
plt.show()
