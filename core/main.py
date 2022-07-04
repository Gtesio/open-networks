import math

from scipy.special import erfcinv

import elements as el
import random
import matplotlib.pyplot as plt

from core.science_utils import dbtolin

net = el.Network("../resources/nodes.json")
net.connect()
print(net.getweightedpath())
print(pow(10, 70/10))
print(dbtolin(net.getweightedpath().loc["A->B", 'SNR']))
print(10 * pow(erfcinv((3/2) * el.BERt), 2) * (el.Rs / el.Bn))
print(2*el.Rs*math.log2(1 + 70*(el.Rs/el.Bn))*1e-9)
print(net.calculate_bit_rate("fe", "shannon-rate"))

'''
conn = []
nodeletters = net.getnodes()
while len(conn) < 100:
    start = random.choice(nodeletters)
    end = random.choice(nodeletters)
    if start != end:
        choice = random.randint(0, 9)
        conn.append(el.Connection(start, end, 1e-3, ))

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

plt.tight_layout()
plt.show()
'''