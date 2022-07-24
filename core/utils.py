import matplotlib.pyplot as plt
import numpy as np


def draw_graph8(conn, steps):
    fig2, (at1, at2) = plt.subplots(1, 2)
    at1.grid(axis="y")  # average bitrate
    at1.set_title("bitrate distribution")
    at2.grid(axis="y")  # total capacity
    at2.set_title("SNR")
    at1.set_ylabel("number of connections")
    at1.set_title("Gbps")
    at2.set_ylabel("number of connections")
    at2.set_xlabel("dB")

    total_cap = 0
    xbr = []
    xsnr = []  # per istogramma
    for c in conn:
        total_cap += c.getbitrate()
        xbr.append(c.getbitrate())
        if c.getsnr() is None:
            xsnr.append(0)
        else:
            xsnr.append(c.getsnr())
    esx = round(max(xbr, default=0))

    at1.set_ylim(0, 100)
    at1.hist(xbr, bins=range(0, esx+50, steps))
    at2.hist(xsnr, bins=20)

    plt.tight_layout()
    plt.show()

    plt.figure()
    plt.ylim(0, 50000)
    plt.bar("Total capacity", total_cap, width=0.5)
    plt.ylabel("Gbps")
    plt.tight_layout()
    plt.show()


def draw_graph82(conn, steps):
    fig2, (at1, at2) = plt.subplots(1, 2)
    at1.grid(axis="y")  # average bitrate
    at2.grid(axis="y")  # total capacity
    at2.set_title("SNR")
    at1.set_ylabel("Gbps")
    at2.set_ylabel("number of connections")
    at2.set_xlabel("dB")

    total_cap = 0
    xbr = []
    xsnr = []  # per istogramma
    for c in conn:
        total_cap += c.getbitrate()
        xbr.append(c.getbitrate())
        if c.getsnr() is None:
            xsnr.append(0)
        else:
            xsnr.append(c.getsnr())

    at1.set_ylim(0, 50000)
    at1.bar("Total capacity", total_cap, width=0.5)
    at2.hist(xsnr, bins=20)

    plt.tight_layout()
    plt.show()
