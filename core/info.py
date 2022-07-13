from science_utils import Rs, df


class SignalInformation:
    def __init__(self, signal_power, path):
        self._signal_power = signal_power
        self._noise_power = 0
        self._latency = 0
        self._path = path.upper()

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
            self._path = self._path[1:]
        else:
            print("Error, path empty")


class Lightpath(SignalInformation):
    def __init__(self, signal_power, path, channel=0):
        super().__init__(signal_power, path)
        self._channel = channel
        self._Rs = Rs
        self._df = df

    def getchannel(self):
        return self._channel

    def setchannel(self, channel):
        self._channel = channel
