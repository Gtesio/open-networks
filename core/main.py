import math

from scipy.special import erfcinv

import elements as el
import random
import matplotlib.pyplot as plt
import numpy as np
from core.utils import draw_graph8, draw_graph82

from core.science_utils import dbtolin, BERt, Rs, Bn

net = el.Network("../resources/223495.json")
net.connect()

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

# random 100 connections
'''
conn = []
nodeletters = net.getnodes()
while len(conn) < 100:
    start = random.choice(nodeletters)
    end = random.choice(nodeletters)
    if start != end:
        conn.append(el.Connection(start, end))
'''
# traffic matrix

nodes = net.getnodes()
utm = np.zeros((len(nodes), len(nodes)))
for i in range(100):
    xlist = list(range(len(nodes)))
    ylist = xlist
    x = random.choice(xlist)
    ylist.remove(x)  # non posso scegliere come destinazione il nodo di partenza
    y = random.choice(ylist)
    utm[x][y] += 100

# cerco la coppia di nodi tra cui c'è più traffico
indexes = np.where(utm == np.amax(utm))
nodebroken = nodes[indexes[1][0]]  # prendo il nodo di destinazione

#  traffic recovery

conn = net.traffic_matrix_stream(utm, 1)
draw_graph8(conn, 10)
net.clear_logger()

net.strong_failure(nodebroken)  # 'taglio' una linea casuale verso quel nodo
conn = net.traffic_matrix_stream(utm, 1)
draw_graph8(conn, 10)

net.traffic_recovery()

conn = net.traffic_matrix_stream(utm, 1)
draw_graph8(conn, 10)

#  lab 8 graph comparison
'''
connessioni = net.traffic_matrix_stream(utm, 1)
draw_graph8(connessioni, 10)

connessioni = net.traffic_matrix_stream(utm, 2)
draw_graph8(connessioni, 5)


net = el.Network("../resources/223495flex.json")
net.connect()

connessioni = net.traffic_matrix_stream(utm, 1)
draw_graph8(connessioni, 20)

connessioni = net.traffic_matrix_stream(utm, 5)
draw_graph8(connessioni, 5)

net = el.Network("../resources/223495shannon.json")
net.connect()

connessioni = net.traffic_matrix_stream(utm, 1)
draw_graph8(connessioni, 30)

connessioni = net.traffic_matrix_stream(utm, 6)
draw_graph8(connessioni, 30)

connessioni = net.traffic_matrix_stream(utm, 7)
draw_graph8(connessioni, 30)
'''
# graph for snr and latency early lab
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
net.freelines()
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
net.freelines()
'''
# es 5 lab 6 e 6 lab 8, average bit rates and total allocated capacity comparison for 3 transceiver tech
'''
fig2, (at1, at2, at3) = plt.subplots(1, 3)
at1.grid(axis="y")  # average bitrate
at1.set_title("average bitrate")
at2.grid(axis="y")  # total capacity
at2.set_title("total capacity")
at1.set_ylabel("number of connections")
at2.set_ylabel("Gbps")

at3.grid(axis="y")  # total capacity
at3.set_title("SNR")
at3.set_ylabel("dB")

net.stream(conn)  # fixed rate
net.freelines()
total_cap = 0
average_br = 0
xlabels = ["fixed-rate", "flex-rate", "shannon-rate"]
xvalues = []
xcap = []
xbr = []
xsnr = []  # per istogramma
for c in conn:
    total_cap += c.getbitrate()
    xbr.append(c.getbitrate())
    if c.getsnr() is None:
        xsnr.append(0)
    else:
        xsnr.append(c.getsnr())

at1.hist(xbr, bins=5, alpha=0.5, label='fixed')
at3.hist(xsnr, bins=20, label='fixed', alpha=0.5)
xbr = []
xsnr = []

xvalues.append(total_cap/len(conn))
xcap.append(total_cap)

net = el.Network("../resources/223495flex.json")  # flexrate
net.connect()
net.stream(conn)
net.freelines()
total_cap = 0
average_br = 0
for c in conn:
    total_cap += c.getbitrate()
    xbr.append(c.getbitrate())
    if c.getsnr() is None:
        xsnr.append(0)
    else:
        xsnr.append(c.getsnr())

at1.hist(xbr, bins=15, alpha=0.5, label='flex')
at3.hist(xsnr, bins=20, label='flex', alpha=0.5)
xbr = []
xsnr = []

xvalues.append(total_cap/len(conn))
xcap.append(total_cap)

net = el.Network("../resources/223495shannon.json")  # shannon rate
net.connect()
net.stream(conn)
total_cap = 0
average_br = 0
for c in conn:
    total_cap += c.getbitrate()
    xbr.append(c.getbitrate())
    if c.getsnr() is None:
        xsnr.append(0)
    else:
        xsnr.append(c.getsnr())

xvalues.append(total_cap/len(conn))
xcap.append(total_cap)

at1.hist(xbr, bins=30, alpha=0.5, label='shannon')
at2.bar(xlabels, xcap)
at1.legend(loc='upper right')
at3.hist(xsnr, bins=20, alpha=0.5, label='shannon')
at3.legend(loc='upper right')
'''

# print graph
'''
plt.tight_layout()
plt.show()
'''