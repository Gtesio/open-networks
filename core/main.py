import elements as el
import info

signal1 = info.SignalInformation(100, "acab")
net = el.Network("../resources/nodes.json")
net.connect()

per = net.findpaths("a", "d")
print(per)

print("start signal lat:", signal1.getlat(), "S noise:", signal1.getnp(), "W path: ", signal1.getpath())
net.propagate(signal1)
print("finish signal lat", signal1.getlat(), "S noise:", signal1.getnp(), "W")

net.draw()