import json
import math


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
        return 1e-9 * signal.getsp() * self._length  # change with better formula later

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


class Network:
    def __init__(self, filename):
        with open(filename) as f:
            network_data = json.load(f)
            nodelist = network_data.keys()
            self._nodes = dict()
            self._lines = dict()
            for n in nodelist:  # aggiungo i nodi alla rete
                nodo = Node(n, network_data[n]["position"], network_data[n]["connected_nodes"])
                for lin in network_data[n]["connected_nodes"]: # aggiungo le linee collegate al nodo corrente
                    label = n+lin
                    linea = Line(label, 0)  # la lunghezza sarà calcolata in seguito
                    self._lines[label] = linea
                self._nodes[n] = nodo
            for lin in self._lines:  # calcolo la lunghezza
                nome = self._lines[lin].getlabel()
                dist = math.sqrt((network_data[nome[0]]["position"][0] - network_data[nome[1]]["position"][0])**2 + (network_data[nome[0]]["position"][1] - network_data[nome[1]]["position"][1])**2)
                # valutare se approssimare la distanza con la funzione round()
                self._lines[lin].setlength(dist)
                print(self._lines[lin].getlength())

            print(self._nodes)
            print(self._lines)


net = Network("../resources/nodes.json")
