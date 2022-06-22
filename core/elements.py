import json
import math
import matplotlib.pyplot as plt


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
                print("Error: line " + nextline + " to " + nextline[1] + " unexistent")


class Line:
    def __init__(self, label, length):
        self._label = label
        self._length = length  # in meters
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
                dist = round(math.sqrt((network_data[nome[0]]["position"][0] - network_data[nome[1]]["position"][0])**2 +
                                       (network_data[nome[0]]["position"][1] - network_data[nome[1]]["position"][1])**2))
            # round() perchè ritengo 1m poco significativo per distanze di decine di km e facilita la lettura dei valori
                self._lines[lin].setlength(dist)
                # print(self._lines[lin].getlabel())

    def connect(self):
        for node in self._nodes:  # collego i nodi impostando nella var successive il dizionario con le relative linee
            lista = self._nodes[node].getconnectednodes()
            nodedict = {}
            for cnode in lista:
                linelabel = self._nodes[node].getlabel() + cnode
                nodedict[linelabel] = self._lines[linelabel]
            self._nodes[node].setsuccessive(nodedict)
        for line in self._lines:  # analogo ma per le linee
            successivenode = line[1]
            successivedict = {successivenode: self._nodes[successivenode]}
            self._lines[line].setsuccessive(successivedict)

    def findpaths(self, start, finish, risultato=None, ricorsione=[]):
        start = start.upper()
        finish = finish.upper()  # per rendere la funzione case-agnostic
        if risultato is None:
            risultato = []
        if start == finish:
            ricorsione.append(start) #questo serve solo ad aggiungere il nome del nodo finale nel risultato
            risultato.append(''.join(ricorsione))
            ricorsione.pop()
        else:
            ricorsione.append(start)
            for node in self._nodes[start].getconnectednodes():
                if node not in ricorsione:
                    self.findpaths(node, finish, risultato, ricorsione)
            ricorsione.pop()
            # pop serve per eliminare l'ultimo elemento della ricorsione una volta che è stato completamente attraversato
            # così da permettere nuovamente l'attraversamento a partire da un percorso precedente differente
        return risultato

    def propagate(self, signal):
        path = signal.getpath()
        self._nodes[path[0]].propagate(signal)
        results = [signal.getnp(), signal.getlat()]
        return results

    def draw(self):
        plt.figure()
        plt.grid()
        plt.xlabel("meters")
        plt.ylabel("meters")
        plt.title("network")
        # faccio prima le linee che i nodi così le linee non vengono disegnate sopra i nodi
        for line in self._lines:
            xx = [self._nodes[line[0]].getposition()[0], self._nodes[line[1]].getposition()[0]]
            yy = [self._nodes[line[0]].getposition()[1], self._nodes[line[1]].getposition()[1]]
            plt.plot(xx, yy, color="b", linewidth=1)
        for node in self._nodes:
            x = self._nodes[node].getposition()[0]
            y = self._nodes[node].getposition()[1]
            plt.plot(x, y, marker="o", color="k", markersize=7)
            plt.annotate(node, (x, y), textcoords="offset points", xytext=(10, 1), weight="bold", backgroundcolor="w",
                         bbox=dict(facecolor="k", alpha=0.05))
        plt.show()
