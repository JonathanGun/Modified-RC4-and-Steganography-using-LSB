import wave
import numpy as np
from steganography.base import Stego
from scipy.io import wavfile
import math

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

    def calculate_psnr(self):
        _, data_original = wavfile.read(self.stego_filepath)
        _, data_stego = wavfile.read(self.stego_out_filepath)
        P0 = np.mean(np.abs(data_original))
        P1 = np.mean(np.abs(data_stego))
        PSNR = 10 * math.log10(P1**2 / (P1**2 + P0**2 - 2*P1*P0))
        output_text = "P0 = {:.3f}\n".format(P0)
        output_text += "P1 = {:.3f}\n".format(P1)
        output_text += "Fidelity = {:.3f}".format(PSNR)
        return output_text
