import json
import math
import matplotlib.pyplot as plt
import pandas as pd
import info


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
        self._state = 1

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

    def setstate(self, state=1):
        self._state = state

    def getstate(self):
        return self._state


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
        self._weighted_path = None

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
        #  generate weighted path pandas dataframe
        indexes = []
        data = {'latency': [], 'noise': [], 'SNR': []}
        for snode in self._nodes:
            for enode in self._nodes:
                if snode != enode:
                    path = self.findpaths(snode, enode)
                    for p in path:
                        signal = info.SignalInformation(1e-3, p)
                        indexes.append('->'.join(p))
                        self.propagate(signal)
                        data['latency'].append(signal.getlat())
                        data['noise'].append(signal.getnp())
                        data['SNR'].append(10 * math.log(signal.getsp() / signal.getnp()))
        self._weighted_path = pd.DataFrame(data, index=indexes)

    def getweightedpath(self):
        if self._weighted_path is None:
            print("weighted path not calculated")
        else:
            return self._weighted_path

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

    def find_best_snr(self, snode, enode):
        if self._weighted_path is None:
            print("weighted path not calculated")
        else:
            ppaths = self.findpaths(snode, enode)  # possible paths
            indexes = []
            for pp in ppaths:  # controllo che tutte le linee del percorso siano libere
                empty = 1
                for i in range(len(pp)-1):
                    line = str(pp[i])+str(pp[i+1])
                    if not self._lines[line].getstate():
                        empty = 0
                if empty:
                    indexes.append('->'.join(pp))
            wdf = self.getweightedpath()
            wdf = wdf.filter(items=indexes, axis=0)
            if wdf.empty:
                return None
            bestsnr = wdf['SNR'].max()
            bestindex = wdf['SNR'].idxmax()
            result = {bestindex: bestsnr}
            return result

    def find_best_lat(self, snode, enode):
        if self._weighted_path is None:
            print("weighted path not calculated")
        else:
            ppaths = self.findpaths(snode, enode)  # possible paths
            indexes = []
            for pp in ppaths:
                empty = 1
                for i in range(len(pp) - 1):
                    line = str(pp[i]) + str(pp[i + 1])
                    if not self._lines[line].getstate():
                        empty = 0
                if empty:
                    indexes.append('->'.join(pp))
            wdf = self.getweightedpath()
            wdf = wdf.filter(items=indexes, axis=0)
            if wdf.empty:
                return None
            bestlat = wdf['latency'].min()
            bestindex = wdf['latency'].idxmin()
            result = {bestindex: bestlat}
            return result

    def stream(self, connections, label='latency'):
        label = label.lower()
        if self._weighted_path is None:
            print("error, connect the network before using stream")
            return
        for con in connections:
            if label == 'latency':
                result = self.find_best_lat(con.getinput(), con.getoutput())
            else:
                result = self.find_best_snr(con.getinput(), con.getoutput())
            if result is None:
                con.setlat(0)
                con.setsnr(None)
            else:
                pathindex = ''.join(result.keys())
                path = pathindex.replace("->", "")
                power = con.getsp()
                signal = info.SignalInformation(power, path)
                self.propagate(signal)
                con.setlat(signal.getlat())
                con.setsnr(self._weighted_path['SNR'][pathindex])
                for i in range(len(path)-1):  # rende la linea occupata
                    line = str(path[i])+str(path[i+1])
                    self._lines[line].setstate(0)
        self.freelines()

    def freelines(self):  # per liberare le linee al termine della funzione stream
        for line in self._lines:
            self._lines[line].setstate(1)

    def getnodes(self):
        return ''.join(self._nodes.keys())


class Connection:
    def __init__(self, input, output, signal_power=1e-3):
        self._input = input
        self._output = output
        self._signal_power = signal_power
        self._latency = 0.0
        self._snr = 0.0

    def getinput(self):
        return self._input

    def getoutput(self):
        return self._output

    def getsp(self):
        return self._signal_power

    def getlat(self):
        return self._latency

    def getsnr(self):
        return self._snr

    def setlat(self, lat):
        self._latency = lat

    def setsnr(self, snr):
        self._snr = snr