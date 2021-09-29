import wave
import numpy as np
from steganography.base import Stego

class Audio(Stego):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stego_out_filepath = "out"
        with open(self.stego_filepath, 'rb') as fd:
            self.audio = fd.read()

    def _hide(self):
        print("hiding", self.secret_bytes[:10], "using", self.key)
        return self._insert_lsb(
                stego_bytes=list(self.audio),
                secret_bytes=self.secret_bytes,
                audio_type=True
            )

    def _extract(self):
        print("extracting", self.audio[44:64], "using", self.key)
        return self._extract_lsb(stego_bytes=list(self.audio), audio_type=True)
