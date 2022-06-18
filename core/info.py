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

