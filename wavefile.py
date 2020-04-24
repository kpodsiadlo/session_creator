import wave

class Wavefile():
    def __init__(self, directory, filename):
        self.path = directory + filename

        #wave.open creates representation of wave file
        with wave.open(self.path) as f:
            (self.nchannels, self.sampwidth, self.framerate, self.nframes,
            self.comptype, self.compname) = f.getparams()
        self.name = filename
        self.length_in_seconds = self.nframes/self.framerate

    def get_info(self):
        return (self.name, self.nchannels, self.sampwidth, self.framerate,
                    self.length_in_seconds)
