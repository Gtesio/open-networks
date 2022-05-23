class SignalInformation:
    def __init__(self, signal_power, path):
        self._signal_power = signal_power
        self._noise_power = 0
        self._latency = 0
        self._path = path

    def getsp(self):
        return self._signal_power

    def setsp(self, power):
        self._signal_power = power

    def getnp(self):
        return self._noise_power

    def setnp(self, power):
        self._noise_power = power

    def getlat(self):
        return self._latency

    def setlat(self, latency):
        self._latency = latency

    def getpath(self):
        return self._path

    def setpath(self, path):
        self._path = path

    def addnoise(self, noise):
        self._noise_power += noise

    def addpower(self, power):
        self._signal_power += power

    def addlatency(self, latency):
        self._latency += latency

    def updpath(self):
        if self._path:
            print("crossed node: ", self._path[0])
            self._path = self._path[1:]
        else:
            print("Error, path empty")


class Node:
    def __init__(self, label, position, connected_nodes):
        self._label = label
        self._position = position
        self._connected_nodes = connected_nodes
        self._successive = {}

    def setlabel(self, label):
        self._label = label

    def getlabel(self):
        return self._label

    def setposition(self, position):
        self._position = position

    def getposition(self):
        return self._position

    def setconnectednodes(self, nodes):
        self._connected_nodes = nodes

    def getconnectednodes(self):
        return self._connected_nodes

    def setsuccessive(self, successive):
        self._successive = successive

    def getsuccessive(self):
        return self._successive

    def propagate(self, signal):
        signal.updpath()
        path = signal.getpath()
        if path:
            nextline = self._label + path[0]
            if nextline in self._successive:
                self._successive[nextline].propagate(signal)
            else:
                print("Line " + nextline + " to " + nextline[1] + " unreachable")
        else:
            print("Destination reached, no more nodes in path")


class Line:
    def __init__(self, label, length):
        self._label = label
        self._length = length # in meters
        self._successive = {}

    def setlabel(self, label):
        self._label = label

    def getlabel(self):
        return self._label

    def setlength(self, length):
        self._length = length

    def getlength(self):
        return self._length

    def setsuccessive(self, dictionary):
        self._successive = dictionary

    def getsuccessive(self):
        return self._successive

    def latencygeneration(self):
        return self._length / 199e6

    def noisegeneration(self, signal):
        return 1e-9 * signal.getsp() * self._length

    def propagate(self, signal):
        print("in line " + self._label)
        path = signal.getpath()
        signal.addlatency(self.latencygeneration())
        signal.addnoise(self.noisegeneration(signal))
        if path:
            if path[0] in self._successive:
                self._successive[path[0]].propagate(signal)
            else:
                print("error, no successive node found")
        else:
            print("error, path is empty")


lineac = Line("ac", 1000000)
nodea = Node("a", (4, 5), "")
nodec = Node("c", (3, 2), "")
signal1 = SignalInformation(100, "ac")
signal2 = SignalInformation(100, "aca")

succ = {"a": nodea, "c": nodec}
lineac.setsuccessive(succ)

succ = {"ac": lineac}
nodea.setsuccessive(succ)

succ = {"ca": lineac}
nodec.setsuccessive(succ)

print("start signal 1", signal1.getlat(), signal1.getnp())
nodea.propagate(signal1)
print("finish signal 1", signal1.getlat(), signal1.getnp())

print("start signal 2", signal2.getlat(), signal2.getnp())
nodea.propagate(signal2)
print("finish signal 2", signal2.getlat(), signal2.getnp())
