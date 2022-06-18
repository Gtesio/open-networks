import elements as el
import info

lineac = el.Line("ac", 1000000)
nodea = el.Node("a", (4, 5), "")
nodec = el.Node("c", (3, 2), "")
signal1 = info.SignalInformation(100, "ac")
signal2 = info.SignalInformation(100, "aca")

succ = {"a": nodea, "c": nodec}
lineac.setsuccessive(succ)

succ = {"ac": lineac}
nodea.setsuccessive(succ)

succ = {"ca": lineac}
nodec.setsuccessive(succ)

print("start signal 1", signal1.getlat(), signal1.getnp(), "path: ", signal1.getpath())
nodea.propagate(signal1)
print("finish signal 1", signal1.getlat(), signal1.getnp())

print("start signal 2", signal2.getlat(), signal2.getnp(), "path: ", signal2.getpath())
nodea.propagate(signal2)
print("finish signal 2", signal2.getlat(), signal2.getnp())