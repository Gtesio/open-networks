import json
import math
import matplotlib.pyplot as plt
import pandas as pd
import info
from scipy.special import erfcinv
from science_utils import lintodb, dbtolin, BERt, Rs, Bn, G, NF, Planck, Freq, Adb, b2, gamma, Alpha, Leff, df


class Node:
    def __init__(self, label, position, connected_nodes, transceiver="fixed-rate"):
        self._label = label
        self._position = position
        self._connected_nodes = connected_nodes
        self._successive = {}
        self._transceiver = transceiver

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

    def settransceiver(self, transceiver="fixed-rate"):
        self._transceiver = transceiver

    def gettransceiver(self):
        return self._transceiver

    def propagate(self, signal):
        signal.updpath()
        path = signal.getpath()
        if path:
            nextline = self._label + path[0]
            if nextline in self._successive:
                self._successive[nextline].propagate(signal)
            else:
                print("Error: line " + nextline + " to " + nextline[1] + " nonexistent")

    def probe(self, signal):  # uguale a propagate ma ignora l'occupazione dei canali
        signal.updpath()
        path = signal.getpath()
        if path:
            nextline = self._label + path[0]
            if nextline in self._successive:
                self._successive[nextline].probe(signal)
            else:
                print("Error: line " + nextline + " to " + nextline[1] + " nonexistent")


class Line:
    def __init__(self, label, length, channels=1):
        self._label = label
        self._length = length  # in meters
        self._successive = {}
        self._state = []  # stato dei canali, 1 = libero, 0 = occupato, indice = canale
        self._n_amplifiers = 0
        for i in range(channels):
            self._state.append(1)
        if length:
            self._n_amplifiers = (length // 80000) + 2

    def setlabel(self, label):
        self._label = label

    def getlabel(self):
        return self._label

    def setlength(self, length):
        self._length = length
        self._n_amplifiers = (self._length // 80000) + 2

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
        channel = signal.getchannel()
        if path:
            if path[0] in self._successive:
                if channel > len(self._state):
                    print("il canale richiesto non esiste")
                    signal.setlat(0)
                    signal.setnp(None)
                else:
                    if self._state[channel]:  # controllo che il canale assegnato al segnale sia libero
                        self._state[channel] = 0
                        signal.addlatency(self.latencygeneration())
                        signal.addnoise(self.noisegeneration(signal))
                        self._successive[path[0]].propagate(signal)
                    else:
                        signal.setlat(0)
                        signal.setnp(None)
                        print("canale occupato")
            else:
                print("error, no successive node found")
        else:
            print("error, path is empty")

    def probe(self, signal):  # uguale a propagate ma ignora l'occupazione dei canali
        path = signal.getpath()
        if path:
            if path[0] in self._successive:
                signal.addlatency(self.latencygeneration())
                signal.addnoise(self.noisegeneration(signal))
                self._successive[path[0]].probe(signal)
            else:
                print("error, no successive node found")
        else:
            print("error, path is empty")

    def setstate(self, channel, state=1):  # imposta lo stato di un singolo canale, default lo libera
        self._state[channel] = state

    def getstate(self):  # ottiene lo stato di tutti i canali
        return self._state

    def freechannels(self):  # libera tutti i canali
        for ch in self._state:
            self._state[ch] = 1

    def ase_generation(self):
        return self._n_amplifiers * (Planck*Freq*Bn*NF*(G-1))

    def nli_generation(self, power):
        a = (16/(27*math.pi))
        ba = pow(math.pi, 2)/2
        bb = (b2*pow(Rs, 2))/Alpha
        bc = pow(len(self._state), 2*(Rs/df))
        b = math.log(ba*bb*bc, 10)
        c = ((gamma*gamma)/(4*Alpha*b2))*(1/pow(Rs, 3))
        nnli = a*b*c  # pag 8 08_OLS.pdf
        nspan = self._n_amplifiers-1
        return power*pow(len(self._state, 3))*nnli*nspan*Bn  # formula da lab 7


class Network:
    def __init__(self, filename):
        with open(filename) as f:
            network_data = json.load(f)
            nodelist = network_data.keys()
            self._nodes = dict()
            self._lines = dict()
            for n in nodelist:  # aggiungo i nodi alla rete
                if "transceiver" in network_data[n]:  # se presente nel json aggiunge il tipo di transceiver
                    nodo = Node(n, network_data[n]["position"], network_data[n]["connected_nodes"], network_data[n]["transceiver"])
                else:
                    nodo = Node(n, network_data[n]["position"], network_data[n]["connected_nodes"])
                for lin in network_data[n]["connected_nodes"]:  # aggiungo le linee collegate al nodo corrente
                    label = n+lin
                    linea = Line(label, 0, 10)  # la lunghezza sarà calcolata in seguito, 10 sono i canali per ex
                    self._lines[label] = linea
                self._nodes[n] = nodo
            for lin in self._lines:  # calcolo la lunghezza
                nome = self._lines[lin].getlabel()
                dist = round(math.sqrt((network_data[nome[0]]["position"][0] - network_data[nome[1]]["position"][0])**2 +
                                       (network_data[nome[0]]["position"][1] - network_data[nome[1]]["position"][1])**2))
            # round()
                # perchè ritengo 1m poco significativo per distanze di decine di km e facilita la lettura dei valori
                self._lines[lin].setlength(dist)
                # print(self._lines[lin].getlabel())
        self._weighted_path = None
        self._route_space = None

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
                        self.probe(signal)
                        data['latency'].append(signal.getlat())
                        data['noise'].append(signal.getnp())
                        data['SNR'].append(lintodb(signal.getsp() / signal.getnp()))  # formula calcolo snr
        self._weighted_path = pd.DataFrame(data, index=indexes)
        self.updateroutespace()

    def updateroutespace(self):
        self._route_space = self._weighted_path.copy()
        indexes = list(self._route_space.index.values)  # percorsi con le "->"
        indexpath = []  # conterrà i percorsi senza le "->"
        choccupancy = None
        for index in indexes:
            indexpath.append("".join(index.split("->")))
        for path in indexpath:
            lineoccupancy = [1] * len(self._lines[path[0]+path[1]].getstate())
            #  lineoccupancy serve per capire se un canale è libero per tutto il percorso (libero a tratti non va bene)
            if choccupancy is None:  # inizializzo choccupancy che andrà nel dataframe
                choccupancy = [[] for i in range(len(lineoccupancy))]
            for s in range(len(path)-1):  # prendo due nodi, se non tolgo 1 prenderei il nodo finale+1 che non esiste
                line = path[s] + path[s+1]  # ABCD --> AB BC CD
                state = self._lines[line].getstate()  # stato dei canali della linea AB, ipotizzo il num canali sia cost
                for ch in range(len(state)):  # numero del canale
                    if not state[ch]:
                        lineoccupancy[ch] = 0  # un canale occupato su un tratto rende la tutta la linea occ sul canale
            for i in range(len(choccupancy)):   # aggiungo le linee occupate
                choccupancy[i].append(lineoccupancy[i])
        for i in range(len(choccupancy)):  # aggiungo le colonne
            self._route_space[i] = choccupancy[i]

    def getweightedpath(self):
        if self._weighted_path is None:
            print("weighted path not calculated")
        else:
            return self._weighted_path

    def getroutespace(self):
        if self._route_space is None:
            print("route space not calculated")
        else:
            return self._route_space

    def findpaths(self, start, finish, risultato=None, ricorsione=None):
        if ricorsione is None:
            ricorsione = []
        start = start.upper()
        finish = finish.upper()  # per rendere la funzione case-agnostic
        if risultato is None:
            risultato = []
        if start == finish:
            ricorsione.append(start)  # questo serve solo ad aggiungere il nome del nodo finale nel risultato
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
        self.updateroutespace()
        return results

    def probe(self, signal):
        path = signal.getpath()
        self._nodes[path[0]].probe(signal)
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
        if self._route_space is None:
            print("route space not calculated")
        else:
            ppaths = self.findpaths(snode, enode)  # possible paths
            indexes = []
            channelstatus = None  # creo
            for pp in ppaths:  # controllo che tutte le linee del percorso siano libere su almeno un canale
                if channelstatus is not None:  # significa che ho fatto il ciclo almeno una volta e quindi preparo la
                    for chs in range(len(channelstatus)):  # variable per l'utilizzo in un nuovo percorso
                        channelstatus[chs] = 1
                for i in range(len(pp)-1):
                    line = str(pp[i])+str(pp[i+1])
                    chstate = self._lines[line].getstate()
                    if channelstatus is None:  # durante il primo ciclo imposto la lunghezza della variabile ipotizzando
                        channelstatus = [[] for i in range(len(chstate))]  # il numero di canali sia costante su tutta la rete
                    for ch in range(len(chstate)):
                        if not chstate[ch]:  # se c'è anche solo un canale occupato su un tratto, tutto il percorso su
                            channelstatus[ch] = 0  # quel canale non è valido
                if 1 in channelstatus:  # se è presente anche solo un canale libero allora il percorso è valido
                    indexes.append('->'.join(pp))
            wdf = self.getroutespace()
            wdf = wdf.filter(items=indexes, axis=0)
            if wdf.empty:
                return None
            bestsnr = wdf['SNR'].max()
            bestindex = wdf['SNR'].idxmax()
            result = {bestindex: bestsnr}
            return result

    def find_best_lat(self, snode, enode):
        if self._route_space is None:
            print("route space not calculated")
        else:
            ppaths = self.findpaths(snode, enode)  # possible paths
            indexes = []
            channelstatus = None  # creo
            for pp in ppaths:  # controllo che tutte le linee del percorso siano libere su almeno un canale
                if channelstatus is not None:  # significa che ho fatto il ciclo almeno una volta e quindi preparo la
                    for chs in range(len(channelstatus)):  # variable per l'utilizzo in un nuovo percorso
                        channelstatus[chs] = 1
                for i in range(len(pp) - 1):
                    line = str(pp[i]) + str(pp[i + 1])
                    chstate = self._lines[line].getstate()
                    if channelstatus is None:  # durante il primo ciclo imposto la lunghezza della variabile ipotizzando
                        channelstatus = [[] for i in range(len(chstate))]  # il numero di canali sia costante su tutta la rete
                    for ch in range(len(chstate)):
                        if not chstate[ch]:  # se c'è anche solo un canale occupato su un tratto, tutto il percorso su
                            channelstatus[ch] = 0  # quel canale non è valido
                if 1 in channelstatus:  # se è presente anche solo un canale libero allora il percorso è valido
                    indexes.append('->'.join(pp))
            wdf = self.getroutespace()
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
                channel = con.getchannel()
                if channel is None:  # non ho assegnato un canale a priori quindi cerco il primo libero
                    rs = self.getroutespace()
                    rs = rs.drop(columns=['SNR', 'latency', 'noise'])  # tolgo le colonne che non servono
                    for i in range(rs.shape[1]):  # ottengo il numero di colonne che corrisponde al num di canali
                        if rs.loc[pathindex, i]:  # assegno il primo libero
                            channel = i
                            break
                signal = info.Lightpath(power, path, channel)
                bitrate = self.calculate_bit_rate(path, self._nodes[path[0].upper()].gettransceiver())
                if bitrate:
                    self.propagate(signal)
                else:  # se ritorna zero rifiuto la connessione
                    signal.setnp(None)
                if signal.getnp() is not None:  # None avviene nel caso il canale specificato non fosse valido
                    con.setlat(signal.getlat())
                    con.setsnr(lintodb(signal.getsp() / signal.getnp()))
                    con.setbitrate(bitrate)
                else:
                    con.setlat(0)
                    con.setsnr(None)
                    con.setbitrate(0)
        self.freelines()

    def freelines(self):  # per liberare le linee al termine della funzione stream
        for line in self._lines:
            self._lines[line].freechannels()
        self.updateroutespace()

    def getnodes(self):
        return ''.join(self._nodes.keys())

    def calculate_bit_rate(self, path, strategy):
        wdf = self.getweightedpath()
        path = '->'.join(path.upper())
        gsnr = dbtolin(wdf.loc[path, 'SNR'])
        if strategy == "fixed-rate":
            if gsnr >= 2*pow(erfcinv(2*BERt), 2)*(Rs/Bn):
                return 100
            else:
                return 0
        if strategy == "flex-rate":
            if gsnr < 2*pow(erfcinv(2*BERt), 2)*(Rs/Bn):
                return 0
            if 2*pow(erfcinv(2*BERt), 2)*(Rs/Bn) <= gsnr < (14/3)*pow(erfcinv((3/2)*BERt), 2)*(Rs/Bn):
                return 100
            if (14/3)*pow(erfcinv(2*BERt), 2)*(Rs/Bn) <= gsnr < 10*pow(erfcinv((8/3)*BERt), 2)*(Rs/Bn):
                return 200
            if gsnr >= 10*pow(erfcinv((8/3)*BERt), 2)*(Rs/Bn):
                return 400
        if strategy == "shannon-rate":
            return 2*Rs*math.log2(1 + gsnr*(Rs/Bn))*1e-9
        print("input strategy invalid")


class Connection:
    def __init__(self, input, output, signal_power=1e-3, channel=None):
        self._input = input
        self._output = output
        self._signal_power = signal_power
        self._latency = 0.0
        self._snr = 0.0
        self._channel = channel
        self._bit_rate = 0

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

    def getchannel(self):
        return self._channel

    def setlat(self, lat):
        self._latency = lat

    def setsnr(self, snr):
        self._snr = snr

    def getbitrate(self):
        return self._bit_rate

    def setbitrate(self, br):
        self._bit_rate = br
