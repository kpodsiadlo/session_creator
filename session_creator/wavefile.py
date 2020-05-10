import wave
import os
import settings as st


class Wavefile():
    def __init__(self, filename=None, directory=None):
        if directory:
            self.filename = filename
            self.path = os.path.join(directory, filename)
            # wave.open creates representation of wave file
            with wave.open(self.path) as f:
                (self.nchannels, self.sampwidth, self.framerate, self.nframes,
                 self.comptype, self.compname) = f.getparams()
            self.name = filename
            self.length_in_seconds = self.nframes/self.framerate
            self.bitrate = self.sampwidth*8
            self.samplerate = self.framerate
            self.format = f"{int(self.sampwidth)*8}bit/{self.framerate}Hz"

        if not directory:
            self.path = filename
            (self.nchannels, self.sampwidth, self.framerate, self.nframes,
             self.comptype, self.compname) = (
                                        None, None, None, None, None, None)
            self.name = filename
            self.length_in_seconds = st.dummy_length

        print(self.name)

    def get_info(self):
        return (self.name, self.nchannels, self.sampwidth, self.framerate,
                self.length_in_seconds)
