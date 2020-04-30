import wave

class Wavefile():
    def __init__(self, filename=None, directory=None):
        if directory:
            self.path = directory + filename
            #wave.open creates representation of wave file
            with wave.open(self.path) as f:
                (self.nchannels, self.sampwidth, self.framerate, self.nframes,
                self.comptype, self.compname) = f.getparams()
            self.name = filename
            self.length_in_seconds = self.nframes/self.framerate

        if not directory:
            self.path = filename
            (self.nchannels, self.sampwidth, self.framerate, self.nframes,
            self.comptype, self.compname) = (None, None, None, None, None, None)
            self.name = filename
            self.length_in_seconds = 2


    def get_info(self):
        return (self.name, self.nchannels, self.sampwidth, self.framerate,
                    self.length_in_seconds)
