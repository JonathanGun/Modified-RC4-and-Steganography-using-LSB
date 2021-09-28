import wave
import numpy as np
from steganography.base import Stego

class Audio(Stego):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open(self.stego_filepath, 'rb') as fd:
            self.audio = fd.read()

    def _hide(self):
        print("hiding", self.secret_bytes[:10], "using", self.key)
        return np.ndarray(
            buffer=np.array(self._insert_lsb(
                stego_bytes=list(self.audio),
                secret_bytes=self.secret_bytes,
            ), dtype="uint8"),
            shape=len(self.audio),
            dtype="uint8",
        )

    def _extract(self):
        print("extracting", self.audio[44:64], "using", self.key)
        return self._extract_lsb(list(self.audio))
