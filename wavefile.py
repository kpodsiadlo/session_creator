import wave

class Wavefile():
    def __init__(self, path):
        with wave.open(path) as f:
            (self.nchannels, self.sampwidth, self.framerate, self.nframes,
            self.comptype, self.compname) = f.getparams()
        self.path = path
        self.length_in_seconds = self.nframes/self.framerate
        print(self.length_in_seconds)
